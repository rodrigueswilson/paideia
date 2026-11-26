# Public article format comparison — 2026-11-26

Status: bounded local experiment, not an application import or a default-format decision. The article's public HTML page is **not** a Zotero-created offline snapshot; Zotero capture and its attachment behavior remain untested.

## Source and method

The comparison uses Murre and Dros (2015), [“Replication and Analysis of Ebbinghaus’ Forgetting Curve”](https://doi.org/10.1371/journal.pone.0120644), PMCID PMC4492928. The [PMC article page](https://pmc.ncbi.nlm.nih.gov/articles/PMC4492928/) supplies HTML and identifies the open-access paper. The versioned JATS XML came from [PMC's open-data service](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) at `https://pmc-oa-opendata.s3.amazonaws.com/PMC4492928.1/PMC4492928.1.xml`. The PDF is the same publisher file used in the [earlier PDF check](PUBLIC_FORGETTING_CURVE_PDF_CHECK_2026-11-25.md). DOI metadata in HTML and XML match. The public HTML was downloaded as raw bytes after a first PowerShell download introduced replacement characters; only the corrected download was measured.

All article files and metrics are in ignored local `data/format-compare/`; no full text or source file is committed. Run `python experiments/compare_public_formats.py data/format-compare` to repeat these measurements after obtaining the same representations. This run used Beautiful Soup 4.14.3 and pypdf 6.7.0; the script reports spot checks, not complete accuracy. The earlier PDF experiment used a different pypdf environment (7.1.1), so the figures below are not its stored output.

| Representation | Bytes | SHA-256 |
|---|---:|---|
| PMC JATS XML v1 | 157,530 | `a9f6e035d048cc01392055934bdbe8b63796923b9405426454ac95d596c47409` |
| PMC HTML page, corrected raw-byte capture | 253,819 | `9084686ad3550961d05a01a022bbb447c8331524215cbbc0f095e5856eb87e3e` |
| Publisher PDF | 807,435 | `2407f0f32f73ae944fd57736d6f825b787719f3c0fd6487f07392833ceee9120` |

## Observations

| Check | JATS XML | PMC HTML | PDF via pypdf 6.7.0 |
|---|---|---|---|
| Text length measured by this adapter | 60,937 characters, abstract and body | 73,438 characters inside `<article>` | 74,463 characters over 23 pages |
| Identifiable tables | 5 `<table-wrap>` | 5 `table.content` | No table objects in the existing adapter |
| Identifiable figures | 7 `<fig>` | 7 `figure.fig` | No figure objects in the existing adapter |
| Identifiable references | 58 `<ref>` | 58 reference-list entries with IDs | No reference objects in the existing adapter |
| Three exact anchors: abstract term, Table 1 value, DOI | All found | All found | All found |
| U+FFFD characters in measured text | 0 | 0 | 0 |

The text-length figures cover different scopes and include markup-derived text such as labels or references; they are not completeness scores. The XML abstract is under `<front>`, separate from `<body>`—an adapter that reads only the body would silently omit it. HTML has navigational and presentation markup around the article, and a sixth HTML `<table>` is an equation layout, so selecting every table element would overcount article data tables. Both cases are concrete reasons to parse structure rather than apply a generic text dump.

The XML and HTML expose table, figure and reference identities directly. This supports more stable section/table/figure locators and citation links than the current plain PDF text adapter. The prior [PDF check](PUBLIC_FORGETTING_CURVE_PDF_CHECK_2026-11-25.md) found that Docling 2.82.0 recovered five table grids and picture records from this PDF, while a word boundary in the abstract was lost. Neither this comparison nor those spot checks verify every cell, citation, equation or figure value. Presence of a figure or caption does not recover plotted data.

## Architecture implication and next check

For an article with a verified public JATS source, prefer that structured representation as a candidate for text, references, tables and figure metadata; retain the original representation and its hash. A public HTML page is a useful second source when XML is unavailable or incomplete. PDF remains necessary for visual inspection and page-based citation, and for articles lacking better representations. This is a proposed routing rule for further testing, not a confirmed default: one paper cannot establish coverage or reliability across publishers.

Before integrating Zotero capture, use a disposable Zotero profile and browser Connector session to verify what it actually saves for this article: attachment type, offline completeness, DOI/URL linkage, and whether the HTML remains parseable after scripts/styles are removed. Do not infer Zotero snapshot quality from this public HTML download. Keep D-013's synthetic-only app boundary unchanged until a separate owner-approved scope and data policy address real sources.
