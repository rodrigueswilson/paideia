"""Small persistence and provenance boundary for the synthetic pilot."""

from __future__ import annotations

from datetime import datetime, timezone
from contextlib import closing, contextmanager
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import sqlite3
from uuid import UUID, NAMESPACE_URL, uuid5

from pypdf import PdfReader

from .sample import QUESTIONS, SAMPLE_LINES, SAMPLE_TITLE, sample_pdf


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _uuid(value: str) -> str:
    return str(UUID(value))


class PilotError(ValueError):
    """A request violates a pilot contract."""


class Store:
    EXTRACTOR = "pypdf:7.1.1:text"

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS sources (
                    id TEXT PRIMARY KEY, title TEXT NOT NULL, origin TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(id),
                    bytes BLOB NOT NULL, imported_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS extractions (
                    id TEXT PRIMARY KEY, document_id TEXT NOT NULL REFERENCES documents(id),
                    extractor TEXT NOT NULL, text TEXT NOT NULL, text_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS objects (
                    id TEXT PRIMARY KEY, extraction_id TEXT NOT NULL REFERENCES extractions(id),
                    position INTEGER NOT NULL, version INTEGER NOT NULL,
                    quote TEXT NOT NULL, question TEXT NOT NULL, expected_answer TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('draft','approved')),
                    origin TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS attempts (
                    attempt_id TEXT PRIMARY KEY, event_id TEXT NOT NULL UNIQUE,
                    presentation_id TEXT NOT NULL, object_id TEXT NOT NULL REFERENCES objects(id),
                    object_version INTEGER NOT NULL,
                    rating TEXT NOT NULL CHECK(rating IN ('matched','partial','not_yet','skip')),
                    used_hint INTEGER NOT NULL CHECK(used_hint IN (0,1)),
                    occurred_at TEXT NOT NULL, received_at TEXT NOT NULL
                );
                """
            )

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.path, timeout=5)
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

    def import_sample(self) -> dict:
        pdf = sample_pdf()
        document_id = sha256(pdf).hexdigest()
        source_id = str(uuid5(NAMESPACE_URL, "paideia:synthetic-learning-note"))
        try:
            reader = PdfReader(BytesIO(pdf), strict=True)
            if len(reader.pages) != 1:
                raise PilotError("The synthetic fixture must have one page")
            text = reader.pages[0].extract_text() or ""
        except Exception as exc:
            raise PilotError("Could not extract the synthetic PDF") from exc
        if any(line not in text for line in SAMPLE_LINES):
            raise PilotError("Synthetic passage fidelity check failed")
        extraction_id = sha256((document_id + self.EXTRACTOR).encode()).hexdigest()
        with self._connect() as db:
            db.execute("INSERT OR IGNORE INTO sources VALUES (?,?,?)", (source_id, SAMPLE_TITLE, "synthetic fixture"))
            db.execute("INSERT OR IGNORE INTO documents VALUES (?,?,?,?)", (document_id, source_id, pdf, _now()))
            db.execute(
                "INSERT OR IGNORE INTO extractions VALUES (?,?,?,?,?,?)",
                (extraction_id, document_id, self.EXTRACTOR, text, sha256(text.encode()).hexdigest(), _now()),
            )
            for position, (quote, qa) in enumerate(zip(SAMPLE_LINES, QUESTIONS, strict=True)):
                question, expected_answer = qa
                object_id = str(uuid5(NAMESPACE_URL, extraction_id + ":" + str(position)))
                db.execute(
                    "INSERT OR IGNORE INTO objects VALUES (?,?,?,?,?,?,?,?,?)",
                    (object_id, extraction_id, position, 1, quote, question, expected_answer, "draft", "fixture-authored"),
                )
            objects = [dict(row) for row in db.execute("SELECT id,position,status FROM objects ORDER BY position")]
        return {"source_id": source_id, "document_id": document_id, "extraction_id": extraction_id, "objects": objects}

    def objects(self) -> list[dict]:
        with self._connect() as db:
            rows = db.execute(
                """SELECT o.id,o.position,o.version,o.quote,o.question,o.expected_answer,
                          o.status,o.origin,e.text_hash,e.extractor,d.id AS document_id
                   FROM objects o JOIN extractions e ON e.id=o.extraction_id
                   JOIN documents d ON d.id=e.document_id ORDER BY o.position"""
            ).fetchall()
        return [dict(row) for row in rows]

    def approve(self, object_id: str) -> dict:
        with self._connect() as db:
            row = db.execute(
                "SELECT o.quote,e.text FROM objects o JOIN extractions e ON e.id=o.extraction_id WHERE o.id=?",
                (object_id,),
            ).fetchone()
            if row is None:
                raise PilotError("Unknown learning object")
            if row["quote"] not in row["text"]:
                raise PilotError("Quotation does not match its extracted passage")
            db.execute("UPDATE objects SET status='approved' WHERE id=?", (object_id,))
        return {"id": object_id, "status": "approved"}

    def next_object(self) -> dict | None:
        with self._connect() as db:
            rows = db.execute(
                """SELECT o.id,o.position,o.version,o.quote,o.question,o.expected_answer,
                          COUNT(a.attempt_id) AS attempt_count,
                          (SELECT rating FROM attempts a2 WHERE a2.object_id=o.id
                           ORDER BY a2.received_at DESC,a2.rowid DESC LIMIT 1) AS last_rating
                   FROM objects o LEFT JOIN attempts a ON a.object_id=o.id
                   WHERE o.status='approved' GROUP BY o.id ORDER BY o.position"""
            ).fetchall()
        if not rows:
            return None
        unseen = [row for row in rows if row["attempt_count"] == 0]
        if unseen:
            chosen = unseen[0]
            rationale = "Next approved passage in the lesson"
        else:
            needs_review = [row for row in rows if row["last_rating"] != "matched"]
            if not needs_review:
                return None
            chosen = needs_review[0]
            rationale = "A previous attempt needs another look; skip is not mastery"
        result = dict(chosen)
        result["rationale"] = rationale
        result["presentation_id"] = str(uuid5(NAMESPACE_URL, chosen["id"] + ":" + str(chosen["attempt_count"])))
        return result

    def record_attempt(self, data: dict) -> dict:
        try:
            attempt_id = _uuid(data["attempt_id"])
            event_id = _uuid(data["event_id"])
            presentation_id = _uuid(data["presentation_id"])
            object_id = str(data["object_id"])
            version = int(data["object_version"])
            rating = str(data["rating"])
            used_hint = data["used_hint"]
            if rating not in {"matched", "partial", "not_yet", "skip"} or type(used_hint) is not bool:
                raise ValueError
        except (KeyError, TypeError, ValueError) as exc:
            raise PilotError("Invalid attempt envelope") from exc
        with self._connect() as db:
            row = db.execute("SELECT version,status FROM objects WHERE id=?", (object_id,)).fetchone()
            if row is None or row["status"] != "approved" or row["version"] != version:
                raise PilotError("Object is missing, unapproved, or stale")
            prior = db.execute("SELECT * FROM attempts WHERE attempt_id=?", (attempt_id,)).fetchone()
            if prior is not None:
                same = all(
                    prior[key] == value
                    for key, value in {
                        "event_id": event_id,
                        "presentation_id": presentation_id,
                        "object_id": object_id,
                        "object_version": version,
                        "rating": rating,
                        "used_hint": int(used_hint),
                    }.items()
                )
                if not same:
                    raise PilotError("Attempt ID already belongs to different data")
                return {"attempt_id": attempt_id, "event_id": event_id, "replayed": True}
            try:
                db.execute(
                    "INSERT INTO attempts VALUES (?,?,?,?,?,?,?,?,?)",
                    (attempt_id, event_id, presentation_id, object_id, version, rating, int(used_hint), _now(), _now()),
                )
            except sqlite3.IntegrityError as exc:
                raise PilotError("Event ID already belongs to another attempt") from exc
        return {"attempt_id": attempt_id, "event_id": event_id, "replayed": False}

    def summary(self) -> dict:
        with self._connect() as db:
            return {
                "sources": db.execute("SELECT COUNT(*) FROM sources").fetchone()[0],
                "documents": db.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
                "objects": db.execute("SELECT COUNT(*) FROM objects").fetchone()[0],
                "approved": db.execute("SELECT COUNT(*) FROM objects WHERE status='approved'").fetchone()[0],
                "attempts": db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0],
            }

    def backup(self, destination: Path) -> None:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as source, closing(sqlite3.connect(destination)) as target:
            source.backup(target)
