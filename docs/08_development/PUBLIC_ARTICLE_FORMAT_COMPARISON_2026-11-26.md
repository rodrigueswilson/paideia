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

## Second publisher check: 2025 Behavioral Sciences paper

The [Kornell and Bjork paper](https://doi.org/10.3390/bs15070924), PMCID PMC12293037, supplied [versioned JATS XML through PMC open data](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) at `https://pmc-oa-opendata.s3.amazonaws.com/PMC12293037.1/PMC12293037.1.xml`. The XML is 78,533 bytes, SHA-256 `f84ec4cd82b096d6224ca57131b5223c9f1a820f79c4064e972c08bf4d279af0`. Its DOI metadata matches the paper and its structure contains zero tables, six figures and 32 references. All six figures are in `<floats-group>` outside `<body>`. The amended script includes that group in extracted text; the checked abstract phrase and Figure 1 caption phrase then match the previously tested PDF. The PDF remains 15 pages, 1,800,383 bytes, SHA-256 `42f1f035d4efd60af710f511a1a9df9cd59a157f7ba183a0e723d6f004fb5876`.

An automated request for [PMC HTML](https://pmc.ncbi.nlm.nih.gov/articles/PMC12293037/) returned a browser-check page rather than article HTML. A direct request to the [publisher HTML](https://www.mdpi.com/2076-328X/15/7/924) returned HTTP 403. The article is visible through web search, so these responses establish an access limitation of this test route, **not** that HTML does not exist. The browser-check response was excluded from article metrics. No CAPTCHA was solved or bypassed. This case also shows why the route must verify that the downloaded document is actually an article before treating it as extracted evidence.

The two JATS documents differ materially: the first paper puts its figures in the body; the second puts them all in a separate floats group. A generic body-only parser would silently drop the second paper's figure captions. Any XML adapter needs explicit handling for front matter, body, back matter, floats and metadata, with a checked locator model.

## Architecture implication and next check

For an article with a verified public JATS source, prefer that structured representation as a candidate for text, references, tables and figure metadata; retain the original representation and its hash. A public HTML page is a useful second source when XML is unavailable or incomplete and can actually be retrieved. PDF remains necessary for visual inspection and page-based citation, and for articles lacking better representations. This is a proposed routing rule for further testing, not a confirmed default: two papers cannot establish coverage or reliability across publishers.

Before integrating Zotero capture, use a disposable Zotero profile and browser Connector session to verify what it actually saves for this article: attachment type, offline completeness, DOI/URL linkage, and whether the HTML remains parseable after scripts/styles are removed. [Zotero's multiple-instance guidance](https://www.zotero.org/support/kb/multiple_instances) says the Connector normally saves to the first opened instance. The owner's regular Zotero instance was already open, so no Connector capture was attempted and no production-library item was changed. Do not infer Zotero snapshot quality from the public HTML download. Keep D-013's synthetic-only app boundary unchanged until a separate owner-approved scope and data policy address real sources.
