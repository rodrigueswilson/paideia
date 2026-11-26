# Extraction quality check — 2026-11-26

Status: bounded experiment for stored extraction runs. It neither integrates a new application path nor approves any extractor, source, quotation or learning object. The public paper remains a separate local check; D-013's application pilot stays synthetic-only.

## Method

`experiments/extraction_quality.py` reads only a versioned SQLite extraction run. It never reopens the PDF or calls a converter. The five cases carry short, visually established reference points: expected page count, an exact passage on a page, column reading order, selected table shape/cells, and whether a figure page needs review. The public-paper case is bound to the previously recorded PDF SHA-256 so its reference points cannot silently be applied to a different document.

The evaluator reports run/document/engine/version IDs and findings without emitting the stored source passages. A **block** applies to the named passage, table, figure or reading-order check, not necessarily the whole document. A **review** finding means the available artifact cannot establish fidelity automatically. A zero-finding result means only the listed checks passed; it does not approve the document or authorize card generation. Generic checks also detect empty expected pages, U+FFFD replacement characters and segments without page locators. Visual truth and unanticipated word-boundary errors still need reference evidence or review.

## Observed run

The quality evaluator ran against the four persisted synthetic fixtures and the already downloaded public PLOS ONE forgetting-curve paper, using both pypdf 7.1.1 and Docling 2.82.0 runs. The paper's PDF and both SQLite databases stayed under ignored `data/`. Four focused quality tests and two existing storage tests passed.

| Case | pypdf finding | Docling finding |
|---|---|---|
| Plain synthetic text | None in selected checks | None in selected checks |
| Two synthetic columns | Reading order does not match the intended left-column-then-right-column order | Same reading-order issue |
| Synthetic table | Required grid/cell structure missing | Selected 3×2 grid and cells matched |
| Synthetic image-only page | No text; required exact passage absent | OCR text exists, but the exact reference passage fails due to punctuation |
| Public forgetting-curve paper | Selected text passage matched; required page-10 table structure and figure representation missing in this adapter | Selected table structure/cells matched; the abstract passage failed exact matching because of a joined word; figure page still needs visual review |

The reported pypdf font-decoding warnings in the previous paper check did **not** produce U+FFFD in stored segments. The apparent replacement glyphs were terminal display encoding. The [earlier report](PUBLIC_FORGETTING_CURVE_PDF_CHECK_2026-11-25.md) and handoff now state this correction. The generic replacement-character rule remains useful but did not fire on this paper; a regression test injects a real U+FFFD and confirms detection.

## Efficient routing implication

The quality result supports **selective escalation**. Text that passes a checked passage and page-locator condition can remain a drafting candidate while a table or figure on the same PDF is routed for structural extraction or visual review. Do not treat a PDF-wide warning as a reason to discard every usable passage. Do not approve a quotation solely because the text exists in an extractor output: compare it with the source page and record the exact run/segment ID.

[Docling's current pipeline options](https://docling-project.github.io/docling/reference/pipeline_options/) expose controls for OCR, table structure, backend text use, layout and resource limits. That supports the proposed routing architecture, but these options have not been benchmarked here and may differ from the installed 2.82.0 experiment version. First define the quality report and checked-citation contract; then compare exact supported configurations on representative, authorized documents before choosing defaults.

## Reproduce

After generating and ingesting the synthetic fixtures as described in the prior proof, run `python experiments/extraction_quality.py --db data/extraction-proof/extractions.sqlite --case table --engine docling`. Use `--case forgetting-curve` with a local SQLite database containing the separately authorized public-paper run. Run `python -m unittest discover -s experiments -p 'test_extraction*.py' -v` after generating the synthetic fixtures. The tests use only temporary synthetic SQLite records for quality regressions and the generated synthetic PDF for existing storage tests.

The remaining limitations are a small reference set, incomplete figure understanding, no generic detector for every OCR or word-boundary error, no captured extractor warnings in the run schema, and no application-level quality policy. These are concrete next gates, not reasons to delay use of verified text passages.
