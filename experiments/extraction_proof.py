"""Synthetic-only extraction, persistence, and retrieval experiment.

This is not the application import path. Output belongs under ignored data/.
"""

from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
from hashlib import sha256
from io import BytesIO
import importlib.metadata
import json
from pathlib import Path
import sqlite3
import time

SCHEMA_VERSION = 1
FIXTURE_PHRASES = {
    "plain": "Retrieval practice checks what can be recalled without looking.",
    "columns": "Left column: source claims need a stable locator.",
    "table": "Review after a delay",
    "scan": "Scanned page needs optical character recognition.",
}


@contextmanager
def connection(path: Path):
    db = sqlite3.connect(path)
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


def create_fixtures(root: Path) -> None:
    """Build text-layer and image-only PDFs containing invented sentences."""
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from PIL import Image, ImageDraw, ImageFont

    root.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(root / "plain.pdf"), pagesize=(612, 792))
    pdf.setFont("Helvetica", 14)
    pdf.drawString(48, 744, FIXTURE_PHRASES["plain"])
    pdf.drawString(48, 714, "Feedback helps correct a response after an attempt.")
    pdf.save()

    pdf = canvas.Canvas(str(root / "columns.pdf"), pagesize=(612, 792))
    pdf.setFont("Helvetica", 10)
    pdf.drawString(35, 744, FIXTURE_PHRASES["columns"])
    pdf.drawString(315, 744, "Right column: a second passage offers a comparison.")
    pdf.drawString(35, 719, "Left follow-up: keep the original passage traceable.")
    pdf.drawString(315, 719, "Right follow-up: compare related ideas carefully.")
    pdf.save()

    pdf = canvas.Canvas(str(root / "table.pdf"), pagesize=(612, 792))
    pdf.setFont("Helvetica", 12)
    cells = [("Concept", "Purpose"), ("Spacing", FIXTURE_PHRASES["table"]), ("Feedback", "Correct an attempted answer")]
    for index, (left, right) in enumerate(cells):
        y = 740 - index * 34
        pdf.drawString(55, y, left)
        pdf.drawString(240, y, right)
    for y in (755, 721, 687, 653):
        pdf.line(45, y, 550, y)
    for x in (45, 230, 550):
        pdf.line(x, 653, x, 755)
    pdf.save()

    image = Image.new("RGB", (1800, 600), "white")
    draw = ImageDraw.Draw(image)
    draw.text((70, 150), FIXTURE_PHRASES["scan"], fill="black", font=ImageFont.load_default(size=42))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    pdf = canvas.Canvas(str(root / "scan.pdf"), pagesize=(612, 792))
    pdf.drawImage(ImageReader(buffer), 35, 430, width=540, height=180)
    pdf.save()


def initialize(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with connection(db_path) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS sources (
                fixture_name TEXT PRIMARY KEY, current_document_hash TEXT
            );
            CREATE TABLE IF NOT EXISTS documents (
                document_hash TEXT PRIMARY KEY, fixture_name TEXT NOT NULL REFERENCES sources(fixture_name),
                byte_size INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY, document_hash TEXT NOT NULL REFERENCES documents(document_hash),
                engine TEXT NOT NULL, engine_version TEXT NOT NULL, settings_json TEXT NOT NULL,
                schema_version INTEGER NOT NULL, artifact_json TEXT NOT NULL, artifact_hash TEXT NOT NULL,
                elapsed_ms REAL NOT NULL, rss_before_mb REAL, rss_after_mb REAL
            );
            CREATE TABLE IF NOT EXISTS segments (
                segment_id TEXT PRIMARY KEY, run_id TEXT NOT NULL REFERENCES runs(run_id),
                ordinal INTEGER NOT NULL, kind TEXT NOT NULL, text TEXT NOT NULL,
                page INTEGER, bbox_json TEXT, source_ref TEXT, quality TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS segment_fts USING fts5(segment_id UNINDEXED, text);
            CREATE TABLE IF NOT EXISTS citations (
                object_id TEXT PRIMARY KEY, fixture_name TEXT NOT NULL REFERENCES sources(fixture_name),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                segment_id TEXT NOT NULL REFERENCES segments(segment_id),
                quote TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('current','stale'))
            );
            """
        )


def _page_and_bbox(item) -> tuple[int | None, str | None]:
    provenance = getattr(item, "prov", None) or []
    if not provenance:
        return None, None
    first = provenance[0]
    bbox = getattr(first, "bbox", None)
    return getattr(first, "page_no", None), json.dumps(bbox.model_dump(mode="json")) if bbox else None


def convert(path: Path, engine: str, converter=None, settings: dict | None = None) -> tuple[dict, list[dict], str, str]:
    settings = settings or {}
    if engine == "pypdf":
        from pypdf import PdfReader

        if set(settings) - {"extraction_mode"} or settings.get("extraction_mode", "plain") not in {"plain", "layout"}:
            raise ValueError("Unsupported pypdf extraction settings")
        version = importlib.metadata.version("pypdf")
        reader = PdfReader(path, strict=True)
        pages = []
        segments = []
        for page_no, page in enumerate(reader.pages, 1):
            page_text = page.extract_text(extraction_mode=settings.get("extraction_mode", "plain")) or ""
            pages.append({"page": page_no, "text": page_text})
            for line in page_text.splitlines():
                if line.strip():
                    segments.append({"kind": "text", "text": line.strip(), "page": page_no, "bbox": None, "source_ref": None, "quality": "text-layer"})
        return {"pages": pages}, segments, version, "plain text per page"

    if engine == "docling":
        from docling_core.types.doc import TableItem, TextItem

        if settings:
            raise ValueError("Docling settings are not wired into this bounded proof")
        version = importlib.metadata.version("docling")
        if converter is None:
            from docling.document_converter import DocumentConverter

            converter = DocumentConverter()
        result = converter.convert(path)
        artifact = result.document.export_to_dict()
        segments = []
        for item, _ in result.document.iterate_items():
            if isinstance(item, TextItem):
                content = item.text.strip()
                kind = str(item.label)
            elif isinstance(item, TableItem):
                content = " | ".join(cell.text for cell in item.data.table_cells if cell.text)
                kind = "table"
            else:
                continue
            if not content:
                continue
            page, bbox = _page_and_bbox(item)
            segments.append({"kind": kind, "text": content, "page": page, "bbox": bbox, "source_ref": item.self_ref, "quality": "converted"})
        return artifact, segments, version, str(result.status)
    raise ValueError(f"Unknown engine: {engine}")


def ingest(db_path: Path, path: Path, engine: str, converter=None, settings: dict | None = None) -> dict:
    """Reuse an exact run; persist new output and searchable segments atomically."""
    initialize(db_path)
    data = path.read_bytes()
    if not data.startswith(b"%PDF-"):
        raise ValueError("Only PDF fixtures are accepted")
    document_hash = sha256(data).hexdigest()
    if engine == "pypdf" and (set(settings or {}) - {"extraction_mode"} or (settings or {}).get("extraction_mode", "plain") not in {"plain", "layout"}):
        raise ValueError("Unsupported pypdf extraction settings")
    if engine == "docling" and settings:
        raise ValueError("Docling settings are not wired into this bounded proof")
    version = importlib.metadata.version(engine)
    settings_json = json.dumps(settings or {}, sort_keys=True)
    run_id = sha256(f"{document_hash}|{engine}|{version}|{settings_json}|{SCHEMA_VERSION}".encode()).hexdigest()
    with connection(db_path) as db:
        existing = db.execute("SELECT run_id FROM runs WHERE run_id=?", (run_id,)).fetchone()
        if existing:
            db.execute("UPDATE sources SET current_document_hash=? WHERE fixture_name=?", (document_hash, path.stem))
            db.execute("UPDATE citations SET status=CASE WHEN run_id IN (SELECT run_id FROM runs WHERE document_hash=?) THEN 'current' ELSE 'stale' END WHERE fixture_name=?", (document_hash, path.stem))
            return {"fixture": path.stem, "engine": engine, "run_id": run_id, "document_hash": document_hash, "reused": True}
    rss_before = None
    rss_after = None
    try:
        import psutil

        rss_before = psutil.Process().memory_info().rss / 1024**2
    except ImportError:
        pass
    started = time.perf_counter()
    artifact, segments, converted_version, conversion_status = convert(path, engine, converter, settings)
    elapsed_ms = (time.perf_counter() - started) * 1000
    if sha256(path.read_bytes()).hexdigest() != document_hash:
        raise ValueError("PDF bytes changed during conversion")
    if rss_before is not None:
        rss_after = psutil.Process().memory_info().rss / 1024**2
    if converted_version != version:
        raise ValueError("Installed extractor version changed during conversion")
    artifact_json = json.dumps(artifact, sort_keys=True, ensure_ascii=False)
    artifact_hash = sha256(artifact_json.encode()).hexdigest()
    with connection(db_path) as db:
        db.execute("INSERT OR IGNORE INTO sources(fixture_name) VALUES (?)", (path.stem,))
        db.execute("INSERT OR IGNORE INTO documents VALUES (?,?,?)", (document_hash, path.stem, len(data)))
        db.execute("UPDATE sources SET current_document_hash=? WHERE fixture_name=?", (document_hash, path.stem))
        db.execute("UPDATE citations SET status='stale' WHERE fixture_name=? AND run_id IN (SELECT run_id FROM runs WHERE document_hash<>?)", (path.stem, document_hash))
        db.execute(
            "INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (run_id, document_hash, engine, version, settings_json, SCHEMA_VERSION, artifact_json, artifact_hash, elapsed_ms, rss_before, rss_after),
        )
        for ordinal, segment in enumerate(segments):
            segment_id = sha256(f"{run_id}:{ordinal}".encode()).hexdigest()
            db.execute(
                "INSERT INTO segments VALUES (?,?,?,?,?,?,?,?,?)",
                (segment_id, run_id, ordinal, segment["kind"], segment["text"], segment["page"], segment["bbox"], segment["source_ref"], segment["quality"]),
            )
            db.execute("INSERT INTO segment_fts VALUES (?,?)", (segment_id, segment["text"]))
    return {
        "fixture": path.stem, "engine": engine, "run_id": run_id, "document_hash": document_hash,
        "reused": False, "segments": len(segments), "elapsed_ms": round(elapsed_ms, 2),
        "rss_before_mb": round(rss_before, 1) if rss_before is not None else None,
        "rss_after_mb": round(rss_after, 1) if rss_after is not None else None,
        "status": conversion_status, "artifact_bytes": len(artifact_json.encode()),
    }


def search(db_path: Path, phrase: str) -> list[dict]:
    """Query only persisted segments; no extractor import or PDF read occurs."""
    query = '"' + phrase.replace('"', '""') + '"'
    with connection(db_path) as db:
        rows = db.execute(
            """SELECT s.segment_id,s.text,s.kind,s.page,s.source_ref,s.quality,
                      r.run_id,r.engine,r.engine_version,r.document_hash,d.fixture_name
               FROM segment_fts f JOIN segments s ON s.segment_id=f.segment_id
               JOIN runs r ON r.run_id=s.run_id JOIN documents d ON d.document_hash=r.document_hash
               WHERE segment_fts MATCH ? ORDER BY d.fixture_name,s.ordinal""",
            (query,),
        ).fetchall()
    return [dict(row) for row in rows]


def cite(db_path: Path, object_id: str, result: dict, quote: str) -> None:
    if quote not in result["text"]:
        raise ValueError("Quotation does not match stored segment")
    with connection(db_path) as db:
        current = db.execute("SELECT current_document_hash FROM sources WHERE fixture_name=?", (result["fixture_name"],)).fetchone()
        if current is None or current[0] != result["document_hash"]:
            raise ValueError("Cannot cite an outdated document version as current")
        db.execute(
            "INSERT INTO citations VALUES (?,?,?,?,?,?)",
            (object_id, result["fixture_name"], result["run_id"], result["segment_id"], quote, "current"),
        )


def backup(db_path: Path, destination: Path) -> None:
    with closing(sqlite3.connect(db_path)) as source, closing(sqlite3.connect(destination)) as target:
        source.backup(target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic-only extraction/storage proof")
    parser.add_argument("action", choices=("generate", "ingest", "search"))
    parser.add_argument("--root", type=Path, default=Path("data/extraction-proof"))
    parser.add_argument("--engine", choices=("pypdf", "docling"))
    parser.add_argument("--phrase")
    args = parser.parse_args()
    fixture_dir = args.root / "fixtures"
    db_path = args.root / "extractions.sqlite"
    if args.action == "generate":
        create_fixtures(fixture_dir)
        print(json.dumps({"fixtures": sorted(path.name for path in fixture_dir.glob("*.pdf"))}))
    elif args.action == "ingest":
        if not args.engine:
            parser.error("--engine is required for ingest")
        converter = None
        if args.engine == "docling":
            from docling.document_converter import DocumentConverter

            converter = DocumentConverter()
        for path in sorted(fixture_dir.glob("*.pdf")):
            print(json.dumps(ingest(db_path, path, args.engine, converter), ensure_ascii=False))
    else:
        if not args.phrase:
            parser.error("--phrase is required for search")
        print(json.dumps(search(db_path, args.phrase), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
