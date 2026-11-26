# Public format routing gate — 2026-11-26

Status: bounded four-paper spot check to guide an extraction experiment. It does not establish general accuracy, change the synthetic-only application boundary, or approve a default extractor.

## Corpus and checks

All four papers are public and open access. The [2015 PLOS ONE forgetting-curve paper](https://doi.org/10.1371/journal.pone.0120644) and [2025 Behavioral Sciences model paper](https://doi.org/10.3390/bs15070924) were checked previously in the [format comparison](PUBLIC_ARTICLE_FORMAT_COMPARISON_2026-11-26.md). The added cases broaden the layout and publisher set: [2013 PLOS ONE retrieval practice study](https://pmc.ncbi.nlm.nih.gov/articles/PMC3827082/) (CC BY) and [2024 BMC Medical Education mnemonic study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11234616/) (CC BY 4.0). Their versioned JATS XML and PDFs came from [PMC's public article datasets](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/). Only hashes, structural counts and short spot-check results are committed; originals and metrics stay in ignored local data.

| Paper / PMCID | XML SHA-256 | PDF SHA-256 | XML tables / figures / references | PDF pages | Checked abstract / figure / table anchors |
|---|---|---|---:|---:|---|
| PLOS 2015 / PMC4492928 | `a9f6e035d048cc01392055934bdbe8b63796923b9405426454ac95d596c47409` | `2407f0f32f73ae944fd57736d6f825b787719f3c0fd6487f07392833ceee9120` | 5 / 7 / 58 | 23 | Three short anchors found in XML, HTML and PDF |
| MDPI 2025 / PMC12293037 | `f84ec4cd82b096d6224ca57131b5223c9f1a820f79c4064e972c08bf4d279af0` | `42f1f035d4efd60af710f511a1a9df9cd59a157f7ba183a0e723d6f004fb5876` | 0 / 6 / 32 | 15 | Abstract and Figure 1 caption phrases found in XML and PDF |
| PLOS 2013 / PMC3827082 | `c5f459e5ae8357c8d25ef26d3358211ed456411cb8a3cfd81a882f6ab19404b6` | `569342fd49d85f6d5b17b9a4752b80bba98f53f93e9c7f1ae5197472305dbf44` | 2 / 2 / 30 | 8 | Abstract phrase, figure-caption term and table value found in XML and PDF |
| BMC 2024 / PMC11234616 | `6cfe9c2c0c97a66107f4f65899a32937e2a9b5ed2abc6ba1e5b80e01c49f7a6b` | `0984d1696bb9e30819bd189999dd9ee604ad56302c6230c11df8b215497f7dc5` | 2 / 1 / 40 | 11 | Abstract phrase, figure-caption phrase and table term found in XML and PDF |

The new XML files were 78,569 and 82,732 bytes. Their PDFs were 545,294 and 1,135,175 bytes. Python's pypdf 6.7.0 and XML parser completed the checks. No U+FFFD character was found in the selected extracted text. These are only exact-anchor spot checks, not a cell-by-cell or page-alignment audit.

## Concrete routing lessons

- **Verify the representation.** Three automated PMC HTML requests in this four-paper set returned a browser-check page rather than article HTML; the first paper's earlier request returned an article. HTML being linked or visible in a browser is not proof that a stable offline article was saved. The owner's ordinary Zotero capture of the first paper contained a stored PDF and a linked catalog page, not an offline HTML snapshot, as detailed in the [format comparison](PUBLIC_ARTICLE_FORMAT_COMPARISON_2026-11-26.md).
- **Read the whole JATS structure.** In the MDPI 2025 paper, all six figures are under `<floats-group>` outside `<body>`. Abstracts are under `<front>`; references under `<back>`. A body-only extraction loses evidence.
- **Do not assume every section has an ID.** All checked tables, figures and references have IDs, but only 41 of 47 sections in the BMC paper have IDs. The six missing IDs include abstract subsections and supplementary material. Section locators need a deterministic path fallback and an explicit `native_id` field that can be null.
- **Keep PDF page evidence separate.** The XML gives structural IDs, while PDF extraction gives page numbers. This check did not align every XML section, cell or figure to PDF pages. A citation should not claim a page solely from an XML ID.

## Stop point and next implementation slice

Four papers from three publisher families found concrete parser and availability failures. That is enough to build a **small, reversible format-aware import experiment**; more corpus collection would have diminishing value before the adapter exists. Accept XML only after validating article identity and required sections; record the source URL, bytes hash, representation kind and extraction version. Extract front/body/back/floats separately and retain native IDs plus fallback locators. Treat linked web pages as links, not stored artifacts. Route to PDF text/layout extraction when XML is absent or a needed element fails validation, and flag figures and uncertain quotations for review. Test this with synthetic fixtures before connecting it to the application.

The gate to reconsider after that slice: can a fresh process retrieve one chosen passage, table, figure caption and reference with correct source and locator from stored artifacts without redownloading or reconverting? The answer should be checked on synthetic fixtures and a bounded public sample. No real learner data or private source import is authorized by this report.
