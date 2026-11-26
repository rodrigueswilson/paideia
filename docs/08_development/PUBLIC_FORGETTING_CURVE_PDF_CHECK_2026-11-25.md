# Public forgetting-curve PDF extraction check — 2026-11-25

Status: one-source, local experiment. It does not change D-013's synthetic-only application pilot, approve a real learner-data policy, or select an extractor.

## Source and handling

Murre, J. M. J., & Dros, J. (2015), [“Replication and Analysis of Ebbinghaus’ Forgetting Curve,” *PLOS ONE*](https://doi.org/10.1371/journal.pone.0120644). This is a modern replication and analysis, **not Ebbinghaus's original book**. The [PMC record](https://pmc.ncbi.nlm.nih.gov/articles/PMC4492928/) states Creative Commons Attribution terms. The publisher's public PDF was downloaded locally from `https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0120644&type=printable`. It is 23 pages, 807,435 bytes, SHA-256 `2407f0f32f73ae944fd57736d6f825b787719f3c0fd6487f07392833ceee9120`.

The PDF, rendered PNGs, logs and SQLite database are under ignored `data/` in this worktree. They are not in Git. No private document, learner event, production collection, or external AI processing service was used. Only source metadata and limited quality observations appear here.

## Local result

Both engines completed on the same PDF and persisted separately identified runs in the experiment's SQLite store. Search in a fresh process found the paper's “method of savings” phrase on PDF page 1 with engine/version and document hash while the original PDF had been temporarily moved away. Search for a numeric table value also returned PDF page 10. The store held both engines' artifacts and segments in about 1.81 MB.

| Check | pypdf 7.1.1 | Docling 2.82.0 |
|---|---|---|
| Processed pages | 23 of 23 | 23 of 23 |
| Projected segments | 938 text lines | 203 segments with text, headings, list items, captions and tables |
| Tables and figures | No structure or bounding boxes in this adapter | 5 tables with structured grids, 32 picture records, bounding boxes on all projected segments |
| Observed conversion time | 0.37 s | 18.48 s |
| Process RSS snapshot | Not measured | About 26 MB before conversion, 1,747 MB after conversion |
| Observed problems | Repeated CFF font-decoding warnings because `fontTools` was absent in the pilot environment; later inspection of stored Unicode found no replacement characters, correcting the initial terminal-display impression. | A word boundary was lost in the opening abstract; output must be checked before exact quotation. |

Timing excludes common setup and uses different Python environments, so it is not a fair speed ratio. RSS is before/after, not peak. This paper is one text-layer PDF and cannot measure scan/OCR reliability or generalize to the owner's source mix.

## Visual spot checks

Rendered PDF pages 1, 8 and 10 were inspected locally. Page 1 visibly separates the first two words of the abstract, whereas Docling joined them. Page 8 has a chart and a 7-row data table; Docling represented that table with an 8×7 grid including headers. Page 10 has a 7-row comparison table above four plotted panels. Docling represented the comparison as an 8×5 grid; the first numeric row and its column associations matched the visible page in the inspected cells. It also recorded two picture items on page 10. The pypdf adapter retained text but not these relationships. This was a spot check, not a complete cell-by-cell accuracy audit or graph-data extraction.

## Architectural reading

The persisted source/document/run/segment pattern worked on an authentic scholarly PDF. Docling's structured tables and locators are useful for this source, but its text still needs normalization and verification. pypdf is a fast text-layer path in this run; its font warnings warrant investigation, while absent table structure is a material limitation for this use. A future quality gate should detect encoding replacement characters if present, broken word boundaries, table/figure requirements and uncertain quotations, then route to review or a different extractor. Figures should not be treated as recovered numeric data merely because a picture item exists.

Next decision: define the minimum quality report and active-run selection for a document, then test a small authorized mix of PDF types under an explicit source-data scope. Keep the actual application pilot synthetic-only until its scope and data policy are changed by the owner.
