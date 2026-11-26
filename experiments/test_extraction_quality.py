"""Regression checks for evidence-level extraction defects."""

from pathlib import Path
from contextlib import closing
import json
import sqlite3
import tempfile
import unittest

from extraction_quality import CASES, check_run


class QualityChecksTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.db_path = Path(temporary.name) / "quality.sqlite"

    def save_run(self, case: str, engine: str, lines: list[tuple[int, str]], artifact: dict | None = None):
        with closing(sqlite3.connect(self.db_path)) as db, db:
            db.executescript("""
                CREATE TABLE documents(document_hash TEXT, fixture_name TEXT);
                CREATE TABLE runs(run_id TEXT, document_hash TEXT, engine TEXT,
                                  engine_version TEXT, settings_json TEXT, artifact_json TEXT);
                CREATE TABLE segments(segment_id TEXT, run_id TEXT, ordinal INTEGER,
                                      kind TEXT, text TEXT, page INTEGER, bbox_json TEXT);
            """)
            document_hash = CASES[case].get("document_hash", "synthetic-hash")
            db.execute("INSERT INTO documents VALUES (?,?)", (document_hash, case))
            db.execute("INSERT INTO runs VALUES (?,?,?,?,?,?)",
                       ("run-1", document_hash, engine, "test-version", "{}", json.dumps(artifact or {})))
            db.executemany("INSERT INTO segments VALUES (?,?,?,?,?,?,?)",
                           [(f"segment-{i}", "run-1", i, "text", text, page, None)
                            for i, (page, text) in enumerate(lines)])

    def codes(self, case: str, engine: str) -> set[str]:
        return {item["code"] for item in check_run(self.db_path, case, engine)["findings"]}

    def test_clean_passage_and_encoding_damage(self):
        phrase = CASES["plain"]["anchors"][0][2]
        self.save_run("plain", "pypdf", [(1, phrase)])
        self.assertEqual(self.codes("plain", "pypdf"), set())
        with closing(sqlite3.connect(self.db_path)) as db, db:
            db.execute("UPDATE segments SET text=text||?", ("\ufffd",))
        self.assertEqual(self.codes("plain", "pypdf"), {"replacement_character"})

    def test_reading_order_flags_rowwise_columns(self):
        order = CASES["columns"]["order"]
        rowwise = [(1, order[0][1]), (1, order[2][1]), (1, order[1][1]), (1, order[3][1])]
        self.save_run("columns", "pypdf", rowwise)
        self.assertIn("reading_order_mismatch", self.codes("columns", "pypdf"))

    def test_table_requires_structure_and_checked_cells(self):
        self.save_run("table", "pypdf", [(1, "Spacing Review after a delay")])
        self.assertIn("required_table_structure_missing", self.codes("table", "pypdf"))

        self.db_path.unlink()
        table = {"prov": [{"page_no": 1}], "data": {"num_rows": 3, "num_cols": 2,
                 "table_cells": [
                     {"start_row_offset_idx": 1, "start_col_offset_idx": 0, "text": "Spacing"},
                     {"start_row_offset_idx": 1, "start_col_offset_idx": 1, "text": "Review after a delay"},
                 ]}}
        self.save_run("table", "docling", [(1, "Spacing | Review after a delay")], {"tables": [table]})
        self.assertEqual(self.codes("table", "docling"), set())
        table["data"]["table_cells"][1]["text"] = "Wrong cell"
        with closing(sqlite3.connect(self.db_path)) as db, db:
            db.execute("UPDATE runs SET artifact_json=?", (json.dumps({"tables": [table]}),))
        self.assertIn("reference_table_cell_mismatch", self.codes("table", "docling"))

    def test_scan_missing_text_and_ocr_punctuation(self):
        self.save_run("scan", "pypdf", [])
        self.assertEqual(self.codes("scan", "pypdf"),
                         {"no_text_on_page", "reference_passage_mismatch"})
        self.db_path.unlink()
        self.save_run("scan", "docling", [(1, "Scanned page needs optical character recognition:")])
        self.assertEqual(self.codes("scan", "docling"), {"reference_passage_mismatch"})

    def test_second_paper_figure_caption_requires_review(self):
        lines = [(page, "Page text") for page in range(1, 16)]
        lines[0] = (1, "For over a century, forgetting research has shown")
        lines[1] = (2, "Figure 1. Adepiction of forgetting in the distribution model.")
        pictures = [{"prov": [{"page_no": 2}]}, {"prov": [{"page_no": 3}]}]
        self.save_run("forgetting-distribution", "docling", lines, {"pictures": pictures})
        self.assertEqual(self.codes("forgetting-distribution", "docling"),
                         {"reference_passage_mismatch", "figure_needs_visual_review"})


if __name__ == "__main__":
    unittest.main()
