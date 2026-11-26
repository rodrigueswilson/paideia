# Second public forgetting paper extraction check — 2026-11-26

Status: bounded local experiment. It does not change the synthetic-only application pilot, approve a default extractor, or verify every sentence and figure.

## Source and handling

Kornell, N., & Bjork, R. A. (2025), [“Why Empirical Forgetting Curves Deviate from Actual Forgetting Rates: A Distribution Model of Forgetting,” *Behavioral Sciences*](https://doi.org/10.3390/bs15070924). The [PubMed Central record](https://pmc.ncbi.nlm.nih.gov/articles/PMC12293037/) identifies the article as open access under CC BY 4.0, with received/revised/accepted dates and an academic editor. It is a theoretical model with supporting empirical evidence about forgetting curves, complementary to the 2015 replication tested earlier.

The PDF was downloaded from [PMC's public open-data service](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) using its article-version PDF object, `https://pmc-oa-opendata.s3.amazonaws.com/PMC12293037.1/PMC12293037.1.pdf`, after the publisher PDF endpoint denied scripted access. The downloaded PDF is 15 pages, 1,800,383 bytes, SHA-256 `42f1f035d4efd60af710f511a1a9df9cd59a157f7ba183a0e723d6f004fb5876`. The versioned object and byte hash identify the exact tested representation. The PDF, SQLite database, renderings, logs and quality JSON are ignored local files, not committed.

## Extraction and quality observations

Both engines completed all 15 pages and stored searchable, versioned runs. A passage in the abstract and a figure-caption term were retrieved from SQLite after the PDF was temporarily moved away, without reconversion. The combined ignored database occupied 868,352 bytes.

| Check | pypdf 7.1.1 | Docling 2.82.0 |
|---|---|---|
| Projected segments | 584 text lines across 15 pages | 145 typed segments across 15 pages |
| Structure | No table or picture objects in this adapter | 10 picture records and no tables; one picture record each on visually inspected figure pages 2 and 3 |
| Selected abstract passage | Exact reference phrase matched on page 1 | Exact reference phrase matched on page 1 |
| Selected Figure 1 caption | Exact short phrase matched on page 2 | Failed exact match because two words were joined |
| Figure 1 and 2 pages | Figure structure absent from the stored pypdf artifact | Picture regions present; interpretation and plotted values still require visual review |
| Conversion time within process | 0.37 s | 14.13 s |
| Process RSS before/after | Not measured | About 27 MB before and 1,672 MB after |

Per-file times exclude common setup and use different environments; they are not a fair cold-start performance ratio. RSS is a before/after snapshot, not peak or incremental model cost. No U+FFFD replacement character was found in either stored run. Neither extractor should be credited with recovering numeric curve data merely from a figure caption or picture region.

Pages 1, 2 and 3 were rendered and visually inspected. Page 1 contains the abstract reference phrase. Page 2 shows Figure 1, a distribution/threshold diagram, and its caption. Page 3 shows Figure 2, a multi-panel plot with histograms, and its caption. These checks establish the selected anchor and figure expectations, not full-page accuracy. The quality case is bound to the exact PDF SHA-256 and flags the Docling caption mismatch and both figure pages for review; it flags the pypdf adapter's lack of figure representation while retaining the two checked text passages.

Docling 2.82.0 was also rerun to inspect its built-in `ConversionResult.confidence`, which our prototype does not currently store. It graded the whole document `excellent` for both `mean_grade` and `low_grade`; page 2 received `excellent`/`excellent`. Yet the checked Figure 1 caption on page 2 had joined words. This shows that Docling's confidence can prioritize review but cannot replace reference-passage or exact-quotation checks. Its table score was `NaN` on this paper; there were no detected tables. [Docling's confidence documentation](https://docling-project.github.io/docling/concepts/confidence_scores/) says to emphasize grades and notes that table scoring is not yet implemented.

## Comparison and next gate

The second paper confirms a useful division of labor: ordinary text can be retrieved automatically, while visual evidence needs a separate representation and review path. It also repeats the joined-word problem seen in the first paper, now in a caption rather than the abstract. That is evidence for passage-level quotation checks, not for rejecting the whole document. No automatic quality rule can confirm the semantic or numerical content of the plots from the stored artifacts used here.

Next, compare exact Docling configurations and resource costs only for the paths justified by these failures: text-layer handling, picture extraction and optional figure understanding. Keep model-generated descriptions separate from verbatim extraction and verify them against the original figure before citing them. A larger authorized corpus would be needed before choosing a default routing policy.
