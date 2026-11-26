"""Synthetic JATS storage/retrieval proof; no network or application integration."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from hashlib import sha256
import importlib.metadata
import re
import sqlite3
from pathlib import Path

from bs4 import BeautifulSoup
from defusedxml.common import DefusedXmlException
from defusedxml import ElementTree as SafeET
from pypdf.errors import PdfReadError


PARSER_VERSION = "jats-projection-1"
MAX_XML_BYTES = 20 * 1024 * 1024
MAX_HTML_BYTES = 20 * 1024 * 1024


class EmptyTextLayer(ValueError):
    """A valid PDF had no text segments for this text-only adapter."""


def _text(element) -> str:
    return re.sub(r"\s+", " ", "".join(element.itertext())).strip()


def _paths(root) -> dict:
    paths = {}

    def visit(element, parent_path: str) -> None:
        counts = {}
        for child in element:
            counts[child.tag] = counts.get(child.tag, 0) + 1
            path = f"{parent_path}/{child.tag}[{counts[child.tag]}]"
            paths[child] = path
            visit(child, path)

    paths[root] = f"/{root.tag}[1]"
    visit(root, paths[root])
    return paths


def project_jats(data: bytes, expected_doi: str) -> list[dict]:
    if len(data) > MAX_XML_BYTES:
        raise ValueError("XML exceeds experiment size limit")
    root = SafeET.fromstring(data, forbid_entities=True, forbid_external=True)
    if root.tag != "article":
        raise ValueError("JATS article root required")
    dois = [_text(x) for x in root.findall(".//article-id") if x.get("pub-id-type") == "doi"]
    if len(dois) != 1 or dois[0].casefold() != expected_doi.casefold():
        raise ValueError("Article DOI does not match registered source")
    if root.find("body") is None:
        raise ValueError("JATS body required")

    paths = _paths(root)
    parents = {child: parent for parent in root.iter() for child in parent}
    segments = []
    for element in root.iter():
        tag = element.tag
        if tag == "p":
            ancestors = []
            current = parents.get(element)
            while current is not None:
                ancestors.append(current.tag)
                current = parents.get(current)
            if not ({"abstract", "body"} & set(ancestors)) or {"table-wrap", "fig", "ref"} & set(ancestors):
                continue
            kind, content = "passage", _text(element)
        elif tag == "sec":
            title = element.find("title")
            kind, content = "section_title", _text(title) if title is not None else ""
        elif tag == "table-wrap":
            cells = [_text(cell) for cell in element.iter() if cell.tag in {"td", "th"}]
            label = element.find("label")
            caption = element.find("caption")
            parts = [_text(label)] if label is not None else []
            parts += [_text(caption)] if caption is not None else []
            parts += cells
            kind, content = "table", " | ".join(part for part in parts if part)
        elif tag == "fig":
            caption = element.find("caption")
            kind, content = "figure_caption", _text(caption) if caption is not None else ""
        elif tag == "ref":
            kind, content = "reference", _text(element)
        else:
            continue
        if content:
            segments.append({
                "kind": kind, "text": content,
                "native_id": element.get("id"), "locator": paths[element],
            })
    return segments


@contextmanager
def _connect(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def initialize(db_path: Path) -> None:
    with _connect(db_path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS sources (
                source_id TEXT PRIMARY KEY, doi TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS representations (
                representation_hash TEXT PRIMARY KEY, kind TEXT NOT NULL, bytes BLOB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS source_representations (
                source_id TEXT NOT NULL REFERENCES sources(source_id),
                representation_hash TEXT NOT NULL REFERENCES representations(representation_hash),
                source_url TEXT NOT NULL,
                PRIMARY KEY (source_id, representation_hash, source_url)
            );
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                representation_hash TEXT NOT NULL REFERENCES representations(representation_hash),
                extractor TEXT NOT NULL, extractor_version TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS segments (
                segment_id TEXT PRIMARY KEY, run_id TEXT NOT NULL REFERENCES runs(run_id),
                ordinal INTEGER NOT NULL, kind TEXT NOT NULL, text TEXT NOT NULL,
                native_id TEXT, locator TEXT NOT NULL, page INTEGER
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS segment_fts USING fts5(segment_id UNINDEXED, text);
        """)
        columns = {row["name"] for row in db.execute("PRAGMA table_info(segments)")}
        if "page" not in columns:
            db.execute("ALTER TABLE segments ADD COLUMN page INTEGER")


def _persist(db_path: Path, source_id: str, doi: str, data: bytes, kind: str,
             source_url: str, extractor: str, version: str, segments: list[dict]) -> dict:
    """Persist one verified representation and extraction in a single transaction."""
    if not source_id or not doi or not source_url:
        raise ValueError("Source ID, DOI and origin are required")
    representation_hash = sha256(data).hexdigest()
    run_id = sha256(f"{representation_hash}|{extractor}|{version}".encode()).hexdigest()
    initialize(db_path)
    with _connect(db_path) as db:
        existing_source = db.execute("SELECT doi FROM sources WHERE source_id=?", (source_id,)).fetchone()
        if existing_source and existing_source["doi"].casefold() != doi.casefold():
            raise ValueError("Source ID already belongs to a different DOI")
        existing_representation = db.execute(
            "SELECT kind FROM representations WHERE representation_hash=?", (representation_hash,)
        ).fetchone()
        if existing_representation and existing_representation["kind"] != kind:
            raise ValueError("Identical bytes cannot have conflicting representation kinds")
        db.execute("INSERT OR IGNORE INTO sources VALUES (?,?)", (source_id, doi))
        db.execute("INSERT OR IGNORE INTO representations VALUES (?,?,?)",
                   (representation_hash, kind, data))
        db.execute("INSERT OR IGNORE INTO source_representations VALUES (?,?,?)",
                   (source_id, representation_hash, source_url))
        reused = db.execute("SELECT 1 FROM runs WHERE run_id=?", (run_id,)).fetchone() is not None
        if not reused:
            db.execute("INSERT INTO runs VALUES (?,?,?,?)",
                       (run_id, representation_hash, extractor, version))
            for ordinal, segment in enumerate(segments):
                segment_id = sha256(f"{run_id}:{ordinal}".encode()).hexdigest()
                db.execute("INSERT INTO segments VALUES (?,?,?,?,?,?,?,?)", (
                    segment_id, run_id, ordinal, segment["kind"], segment["text"],
                    segment["native_id"], segment["locator"], segment.get("page"),
                ))
                db.execute("INSERT INTO segment_fts VALUES (?,?)", (segment_id, segment["text"]))
    return {"run_id": run_id, "representation_hash": representation_hash,
            "segments": len(segments), "reused": reused}


def ingest_jats(db_path: Path, source_id: str, doi: str, path: Path, source_url: str) -> dict:
    """Persist exact JATS bytes and projection; reuse an identical run."""
    data = path.read_bytes()
    segments = project_jats(data, doi)
    return _persist(db_path, source_id, doi, data, "jats_xml", source_url,
                    "jats", PARSER_VERSION, segments)


def _html_locator(element, article) -> str:
    parts = []
    current = element
    while current is not None:
        siblings = [s for s in current.previous_siblings if getattr(s, "name", None) == current.name]
        parts.append(f"{current.name}[{len(siblings) + 1}]")
        if current is article:
            break
        current = current.parent
    return "html:/" + "/".join(reversed(parts))


def project_html(data: bytes, expected_doi: str) -> list[dict]:
    if len(data) > MAX_HTML_BYTES:
        raise ValueError("HTML exceeds experiment size limit")
    soup = BeautifulSoup(data, "html.parser")
    article = soup.select_one("article")
    doi_meta = soup.select_one('meta[name="citation_doi"]')
    doi = doi_meta.get("content", "") if doi_meta else ""
    if article is None or doi.casefold() != expected_doi.casefold():
        raise ValueError("HTML article or matching DOI missing")
    segments = []
    for element in article.descendants:
        tag = getattr(element, "name", None)
        if tag == "p":
            if element.find_parent(["table", "figure", "li"]):
                continue
            kind, content = "passage", element.get_text(" ", strip=True)
        elif tag == "section":
            title = element.find(re.compile(r"^h[1-6]$"))
            kind, content = "section_title", title.get_text(" ", strip=True) if title else ""
        elif tag == "table":
            cells = [cell.get_text(" ", strip=True) for cell in element.select("th, td")]
            kind, content = "table", " | ".join(cell for cell in cells if cell)
        elif tag == "figure":
            caption = element.select_one("figcaption, .caption")
            kind, content = "figure_caption", caption.get_text(" ", strip=True) if caption else ""
        elif tag == "li" and element.find_parent(class_="ref-list"):
            kind, content = "reference", element.get_text(" ", strip=True)
        else:
            continue
        if content:
            segments.append({"kind": kind, "text": content,
                             "native_id": element.get("id"),
                             "locator": _html_locator(element, article)})
    if not segments:
        raise ValueError("HTML article has no extractable segments")
    return segments


def ingest_html(db_path: Path, source_id: str, doi: str, path: Path, source_url: str) -> dict:
    data = path.read_bytes()
    segments = project_html(data, doi)
    version = f"beautifulsoup4-{importlib.metadata.version('beautifulsoup4')}-html.parser-1"
    return _persist(db_path, source_id, doi, data, "html", source_url,
                    "html", version, segments)


def ingest_pdf(db_path: Path, source_id: str, doi: str, path: Path, source_url: str) -> dict:
    data = path.read_bytes()
    if not data.startswith(b"%PDF-"):
        raise ValueError("PDF signature missing")
    from extraction_proof import convert

    _, extracted, version, _ = convert(path, "pypdf")
    lines_by_page = {}
    segments = []
    for item in extracted:
        page = item["page"]
        lines_by_page[page] = lines_by_page.get(page, 0) + 1
        segments.append({"kind": "pdf_text", "text": item["text"],
                         "native_id": None, "locator": f"pdf:page:{page}:line:{lines_by_page[page]}",
                         "page": page})
    if not segments:
        raise EmptyTextLayer("PDF text layer empty")
    if sha256(path.read_bytes()).hexdigest() != sha256(data).hexdigest():
        raise ValueError("PDF bytes changed during conversion")
    return _persist(db_path, source_id, doi, data, "pdf", source_url,
                    "pypdf", f"{version}-plain", segments)


@dataclass(frozen=True)
class Candidate:
    kind: str
    source_url: str
    path: Path | None = None
    link_mode: str = "stored"


def route(db_path: Path, source_id: str, doi: str, candidates: list[Candidate]) -> dict:
    """Select verified local XML/HTML, then PDF text; return explicit review flags."""
    flags = []
    for kind in ("jats_xml", "html", "pdf"):
        for candidate in (item for item in candidates if item.kind == kind):
            if candidate.link_mode == "linked_url":
                flags.append(f"{kind}_link_only")
                continue
            if candidate.link_mode != "stored" or candidate.path is None or not candidate.path.is_file():
                flags.append(f"{kind}_unavailable")
                continue
            try:
                if kind == "jats_xml":
                    projected = project_jats(candidate.path.read_bytes(), doi)
                    result = ingest_jats(db_path, source_id, doi, candidate.path, candidate.source_url)
                elif kind == "html":
                    projected = project_html(candidate.path.read_bytes(), doi)
                    result = ingest_html(db_path, source_id, doi, candidate.path, candidate.source_url)
                else:
                    result = ingest_pdf(db_path, source_id, doi, candidate.path, candidate.source_url)
                    projected = []
            except EmptyTextLayer:
                flags.append("pdf_no_text_layer")
                continue
            except (ValueError, SafeET.ParseError, DefusedXmlException, PdfReadError):
                flags.append(f"{kind}_rejected")
                continue
            if kind == "pdf":
                flags += ["pdf_identity_unverified", "pdf_structure_review"]
            else:
                if any(s["kind"] == "section_title" and not s["native_id"] for s in projected):
                    flags.append("section_locator_fallback")
                if any(s["kind"] == "figure_caption" for s in projected):
                    flags.append("figure_evidence_review")
                if any(s["kind"] == "table" for s in projected):
                    flags.append("table_structure_review")
                if kind == "html":
                    flags.append("html_structure_review")
            return {"status": "selected", "kind": kind, "review_flags": flags, **result}
    return {"status": "needs_review", "kind": None, "review_flags": flags or ["no_candidates"]}


def search(db_path: Path, run_id: str, phrase: str) -> list[dict]:
    """Search persisted segments; original file and parser are not needed."""
    query = '"' + phrase.replace('"', '""') + '"'
    with _connect(db_path) as db:
        rows = db.execute("""
            SELECT s.segment_id,s.kind,s.text,s.native_id,s.locator,s.page,
                   r.run_id,r.representation_hash,r.extractor_version
            FROM segment_fts f JOIN segments s ON s.segment_id=f.segment_id
            JOIN runs r ON r.run_id=s.run_id
            WHERE segment_fts MATCH ? AND s.run_id=? ORDER BY s.ordinal
        """, (query, run_id)).fetchall()
    return [dict(row) for row in rows]


def verify_quote(result: dict, quote: str) -> bool:
    return bool(quote) and quote in result["text"]
