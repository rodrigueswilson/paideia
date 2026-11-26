"""Persistence contracts for the synthetic extraction proof."""

from pathlib import Path
from contextlib import closing
import importlib.metadata
import shutil
import sqlite3
import tempfile
import unittest

from extraction_proof import backup, cite, ingest, search


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "extraction-proof" / "fixtures" / "plain.pdf"
PHRASE = "Retrieval practice checks what can be recalled without looking."


class StorageProofTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pdf = self.root / "plain.pdf"
        shutil.copyfile(FIXTURE, self.pdf)
        self.db = self.root / "proof.sqlite"

    def test_reuse_search_restart_backup_and_stale_citation(self):
        first = ingest(self.db, self.pdf, "pypdf")
        self.assertFalse(first["reused"])
        same = ingest(self.db, self.pdf, "pypdf")
        self.assertTrue(same["reused"])
        self.assertEqual(first["run_id"], same["run_id"])

        # Search opens a fresh connection and reads no PDF bytes or extractor.
        self.pdf.rename(self.root / "hidden.pdf")
        found = search(self.db, PHRASE)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["page"], 1)
        self.assertEqual(found[0]["engine_version"], importlib.metadata.version("pypdf"))
        cite(self.db, "object-1", found[0], PHRASE)
        with self.assertRaises(ValueError):
            cite(self.db, "object-2", found[0], "Invented quote")

        backup_path = self.root / "backup.sqlite"
        backup(self.db, backup_path)
        self.assertEqual(search(backup_path, PHRASE), found)
        with closing(sqlite3.connect(backup_path)) as restored:
            self.assertEqual(restored.execute("SELECT status FROM citations").fetchone()[0], "current")

        (self.root / "hidden.pdf").rename(self.pdf)
        with self.pdf.open("ab") as output:
            output.write(b"\n% Synthetic revision\n")
        changed = ingest(self.db, self.pdf, "pypdf")
        self.assertNotEqual(changed["document_hash"], first["document_hash"])
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT status FROM citations").fetchone()[0], "stale")
        with self.assertRaises(ValueError):
            cite(self.db, "object-3", found[0], PHRASE)

        self.pdf.write_bytes(FIXTURE.read_bytes())
        reused = ingest(self.db, self.pdf, "pypdf")
        self.assertTrue(reused["reused"])
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT status FROM citations").fetchone()[0], "current")

    def test_settings_create_distinct_run(self):
        first = ingest(self.db, self.pdf, "pypdf")
        second = ingest(self.db, self.pdf, "pypdf", settings={"extraction_mode": "layout"})
        self.assertNotEqual(first["run_id"], second["run_id"])


if __name__ == "__main__":
    unittest.main()
