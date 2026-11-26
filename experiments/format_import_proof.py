"""Synthetic JATS storage/retrieval proof; no network or application integration."""

from __future__ import annotations

from contextlib import contextmanager
from hashlib import sha256
import re
import sqlite3
from pathlib import Path

from defusedxml import ElementTree as SafeET


PARSER_VERSION = "jats-projection-1"
MAX_XML_BYTES = 20 * 1024 * 1024


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
                native_id TEXT, locator TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS segment_fts USING fts5(segment_id UNINDEXED, text);
        """)


def ingest_jats(db_path: Path, source_id: str, doi: str, path: Path, source_url: str) -> dict:
    """Persist exact bytes and projection atomically; reuse an identical run."""
    data = path.read_bytes()
    segments = project_jats(data, doi)
    representation_hash = sha256(data).hexdigest()
    run_id = sha256(f"{representation_hash}|{PARSER_VERSION}".encode()).hexdigest()
    initialize(db_path)
    with _connect(db_path) as db:
        existing_source = db.execute("SELECT doi FROM sources WHERE source_id=?", (source_id,)).fetchone()
        if existing_source and existing_source["doi"].casefold() != doi.casefold():
            raise ValueError("Source ID already belongs to a different DOI")
        db.execute("INSERT OR IGNORE INTO sources VALUES (?,?)", (source_id, doi))
        db.execute("INSERT OR IGNORE INTO representations VALUES (?,?,?)",
                   (representation_hash, "jats_xml", data))
        db.execute("INSERT OR IGNORE INTO source_representations VALUES (?,?,?)",
                   (source_id, representation_hash, source_url))
        reused = db.execute("SELECT 1 FROM runs WHERE run_id=?", (run_id,)).fetchone() is not None
        if not reused:
            db.execute("INSERT INTO runs VALUES (?,?,?,?)",
                       (run_id, representation_hash, "jats", PARSER_VERSION))
            for ordinal, segment in enumerate(segments):
                segment_id = sha256(f"{run_id}:{ordinal}".encode()).hexdigest()
                db.execute("INSERT INTO segments VALUES (?,?,?,?,?,?,?)", (
                    segment_id, run_id, ordinal, segment["kind"], segment["text"],
                    segment["native_id"], segment["locator"],
                ))
                db.execute("INSERT INTO segment_fts VALUES (?,?)", (segment_id, segment["text"]))
    return {"run_id": run_id, "representation_hash": representation_hash,
            "segments": len(segments), "reused": reused}


def search(db_path: Path, run_id: str, phrase: str) -> list[dict]:
    """Search persisted segments; original file and parser are not needed."""
    query = '"' + phrase.replace('"', '""') + '"'
    with _connect(db_path) as db:
        rows = db.execute("""
            SELECT s.segment_id,s.kind,s.text,s.native_id,s.locator,
                   r.run_id,r.representation_hash,r.extractor_version
            FROM segment_fts f JOIN segments s ON s.segment_id=f.segment_id
            JOIN runs r ON r.run_id=s.run_id
            WHERE segment_fts MATCH ? AND s.run_id=? ORDER BY s.ordinal
        """, (query, run_id)).fetchall()
    return [dict(row) for row in rows]


def verify_quote(result: dict, quote: str) -> bool:
    return bool(quote) and quote in result["text"]
