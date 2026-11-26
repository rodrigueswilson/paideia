# Synthetic extraction and storage proof — 2026-11-25

Status: bounded experiment under D-013/D-014. No real sources were opened, no application import path changed, and no extractor adoption decision is implied.

## Reproduce

The script `experiments/extraction_proof.py` creates four invented one-page PDFs in ignored `data/extraction-proof/fixtures/`. It writes extracted artifacts, segments, FTS5 index and citations to an ignored SQLite database. Run `generate`, then `ingest --engine pypdf` and `ingest --engine docling`, then `search --phrase "Retrieval practice checks what can be recalled without looking."`. The Docling command needs an environment with Docling and its model assets; the pypdf command needs pypdf. No experiment output is committed.

Test the persistence contract with `python -m unittest discover -s experiments -p test_extraction_proof.py -v` in a pypdf environment after generating fixtures. The test uses a temporary database and checks exact-run reuse, a distinct run for pypdf layout mode, query from a new connection with the PDF moved away, exact quotation validation, backup/restore, stale citation after changed bytes, and reuse after restoring original bytes.

## Observed results

Host experiment versions: Docling 2.82.0 with docling-core 2.70.2, pypdf 7.1.1 in the pilot virtual environment. Four local synthetic PDFs, one page each. Run IDs include document SHA-256, engine, exact version, settings JSON and output schema version. These runs were successful; the two storage tests passed. The SQLite database for both extractors and four fixtures occupied 81,920 bytes. All generated PDFs and the database remain ignored locally.

| Fixture | pypdf 7.1.1 | Docling 2.82.0 | Fidelity observation |
|---|---:|---:|---|
| Plain text | 2 segments, 1.35 ms | 2 segments, 167 ms | Both retained the exact target sentence and page 1. |
| Two columns | 4 lines, 85.85 ms | 1 combined segment, 3,244 ms | Both yielded row-wise reading order for this fixture, not column-wise reading order. |
| Drawn table | 6 lines, 1.56 ms | 1 table segment, 334 ms | Docling's stored structured artifact has a 3×2 grid with 6 cells. pypdf gave text without cell relationships. |
| Image-only scan | 0 segments, 1.24 ms | 1 segment, 370 ms | Docling OCR recovered the words but changed the final period to a colon; an exact quotation check would fail. |

Conversion times above are per-file measurements inside separate long-lived interpreter processes, not comparable cold-start or peak-resource benchmarks. The first pypdf file includes import initialization. Docling's converter was initialized before per-file timing. Docling process RSS before/after conversion rose from about 596 MB to 1,592 MB on the first file and ended near 1,750 MB after all four; these are snapshots, not peak memory or incremental model cost. The pilot virtual environment did not include `psutil`, so pypdf RSS was not measured. Install footprint was not measured. No ranking should be inferred from these timings alone.

The persisted plain-text phrase was retrieved in a separate process for both runs, with fixture ID, document hash, engine/version, segment ID, page, text and Docling source reference. pypdf has no bounding box or structured source reference in this adapter. The Docling artifact retained 5 projected bounding boxes across the four PDFs. A backup database returned the same result and citation state in the storage test. A changed-byte document version left the old run and citation intact, marking the citation stale; an unmatched quotation and an outdated document version were rejected for a new citation.

## Architecture implications and next gate

The versioned SQLite contract is practical at this scale and supports repeated retrieval without conversion. The adapter still needs explicit source identity, robust quality flags, extraction-error storage, and a choice of active run when multiple extractors index the same document. A text-layer fast path with a layout/OCR escalation is plausible, but this small artificial set cannot select an extractor policy. The scan punctuation error and two-column order error show why quality checks and human review must precede approved learning objects.

Next, keep the design PR in draft and review this evidence. For an adoption decision, test exact current package versions in an isolated environment, record dependency/license/security and model asset footprint, and evaluate a small *explicitly authorized* representative corpus only after a separate source-data approval. The owner/lead can then approve a database contract and extractor routing strategy before connecting draft object generation.

Primary API context: [Docling v2 document export](https://docling-project.github.io/docling/v2/), [Docling serialization](https://docling-project.github.io/docling/concepts/serialization/), [Docling installation](https://docling-project.github.io/docling/getting_started/installation/).
