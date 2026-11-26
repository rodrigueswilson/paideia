"""Read-only quality checks for the extraction proof's stored runs.

These checks evaluate selected evidence, not the truth of an entire document.
The public-paper reference points were checked against rendered PDF pages.
"""

from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3


PUBLIC_SHA256 = "2407f0f32f73ae944fd57736d6f825b787719f3c0fd6487f07392833ceee9120"

CASES = {
    "plain": {
        "pages": 1,
        "anchors": [("plain_sentence", 1, "Retrieval practice checks what can be recalled without looking.")],
    },
    "columns": {
        "pages": 1,
        "anchors": [("left_claim", 1, "Left column: source claims need a stable locator.")],
        "order": [("left_claim", "Left column: source claims need a stable locator."),
                  ("left_followup", "Left follow-up: keep the original passage traceable."),
                  ("right_claim", "Right column: a second passage offers a comparison."),
                  ("right_followup", "Right follow-up: compare related ideas carefully.")],
    },
    "table": {
        "pages": 1,
        "tables": [{"page": 1, "rows": 3, "cols": 2,
                    "cells": [(1, 0, "Spacing"), (1, 1, "Review after a delay")]}],
    },
    "scan": {
        "pages": 1,
        "anchors": [("scan_sentence", 1, "Scanned page needs optical character recognition.")],
    },
    "forgetting-curve": {
        "pages": 23,
        "document_hash": PUBLIC_SHA256,
        "anchors": [("abstract_open", 1, "We present a successful replication")],
        "tables": [{"page": 10, "rows": 8, "cols": 5,
                    "cells": [(1, 0, "20 min"), (1, 1, "0.582"), (1, 4, "0.472")]}],
        "figures": [10],
    },
}


def _table_page(table: dict) -> int | None:
    provenance = table.get("prov") or []
    return provenance[0].get("page_no") if provenance else None


def _cell_map(table: dict) -> dict[tuple[int, int], str]:
    return {
        (cell["start_row_offset_idx"], cell["start_col_offset_idx"]): cell.get("text", "").strip()
        for cell in table.get("data", {}).get("table_cells", [])
    }


def check_run(db_path: Path, fixture: str, engine: str, run_id: str | None = None) -> dict:
    """Return only derived findings and IDs; do not emit stored source passages."""
    if fixture not in CASES:
        raise ValueError(f"Unknown quality case: {fixture}")
    expected = CASES[fixture]
    with closing(sqlite3.connect(db_path)) as db:
        db.row_factory = sqlite3.Row
        if run_id:
            run = db.execute(
                """SELECT r.*, d.fixture_name FROM runs r JOIN documents d ON d.document_hash=r.document_hash
                   WHERE r.run_id=? AND d.fixture_name=? AND r.engine=?""", (run_id, fixture, engine)
            ).fetchone()
        else:
            run = db.execute(
                """SELECT r.*, d.fixture_name FROM runs r JOIN documents d ON d.document_hash=r.document_hash
                   WHERE d.fixture_name=? AND r.engine=? AND r.settings_json='{}' ORDER BY r.rowid DESC LIMIT 1""",
                (fixture, engine),
            ).fetchone()
        if run is None:
            raise ValueError("Matching stored run not found")
        segments = [dict(row) for row in db.execute(
            "SELECT segment_id,ordinal,kind,text,page,bbox_json FROM segments WHERE run_id=? ORDER BY ordinal",
            (run["run_id"],),
        )]
        artifact = json.loads(run["artifact_json"])

    findings = []

    def finding(code: str, level: str, target: str, **detail) -> None:
        findings.append({"code": code, "level": level, "target": target, **detail})

    if expected.get("document_hash") and run["document_hash"] != expected["document_hash"]:
        raise ValueError("Stored document hash does not match the visually checked PDF")

    represented_pages = {segment["page"] for segment in segments if segment["text"].strip()}
    for page in range(1, expected["pages"] + 1):
        if page not in represented_pages:
            finding("no_text_on_page", "block", f"page:{page}")

    damaged = [segment for segment in segments if "\ufffd" in segment["text"]]
    if damaged:
        finding("replacement_character", "review", "text", affected_segments=len(damaged),
                pages=sorted({segment["page"] for segment in damaged if segment["page"] is not None}))

    unlocated = sum(segment["page"] is None for segment in segments)
    if unlocated:
        finding("missing_page_locator", "review", "text", affected_segments=unlocated)

    anchor_results = {}
    for label, page, phrase in expected.get("anchors", []):
        matched = [segment for segment in segments if segment["page"] == page and phrase in segment["text"]]
        anchor_results[label] = {"page": page, "matched": bool(matched),
                                 "segment_ids": [segment["segment_id"] for segment in matched]}
        if not matched:
            finding("reference_passage_mismatch", "block", f"anchor:{label}", page=page)

    if expected.get("order"):
        text = "\n".join(segment["text"] for segment in segments)
        positions = [text.find(phrase) for _, phrase in expected["order"]]
        if -1 in positions or positions != sorted(positions):
            finding("reading_order_mismatch", "block", "text:reading_order")

    tables = artifact.get("tables", [])
    table_results = []
    for index, requirement in enumerate(expected.get("tables", []), 1):
        matching = [table for table in tables if _table_page(table) == requirement["page"]
                    and table.get("data", {}).get("num_rows") == requirement["rows"]
                    and table.get("data", {}).get("num_cols") == requirement["cols"]]
        if not matching:
            table_results.append({"page": requirement["page"], "structure_matched": False, "cells_matched": False})
            finding("required_table_structure_missing", "block", f"table:{index}", page=requirement["page"])
            continue
        cells = _cell_map(matching[0])
        mismatches = [(row, col) for row, col, value in requirement["cells"] if cells.get((row, col)) != value]
        table_results.append({"page": requirement["page"], "structure_matched": True,
                              "cells_matched": not mismatches})
        if mismatches:
            finding("reference_table_cell_mismatch", "block", f"table:{index}", page=requirement["page"],
                    positions=mismatches)

    figures = artifact.get("pictures", [])
    for page in expected.get("figures", []):
        count = sum(_table_page(picture) == page for picture in figures)
        if count == 0:
            finding("figure_not_represented", "block", f"figure:page:{page}")
        else:
            finding("figure_needs_visual_review", "review", f"figure:page:{page}", picture_records=count)

    return {
        "fixture": fixture, "engine": engine, "engine_version": run["engine_version"],
        "document_hash": run["document_hash"], "run_id": run["run_id"],
        "segment_count": len(segments), "pages_with_text": len(represented_pages),
        "anchors": anchor_results, "tables": table_results, "findings": findings,
        "summary": {"blocked_checks": sum(item["level"] == "block" for item in findings),
                    "review_checks": sum(item["level"] == "review" for item in findings)},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check stored extraction evidence without reading the source PDF")
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--case", choices=sorted(CASES), required=True)
    parser.add_argument("--engine", choices=("pypdf", "docling"), required=True)
    parser.add_argument("--run-id")
    args = parser.parse_args()
    print(json.dumps(check_run(args.db, args.case, args.engine, args.run_id), indent=2))


if __name__ == "__main__":
    main()
