# Synthetic format routing proof — 2026-11-26

Status: bounded experiment outside the application. All fixtures and tests are synthetic. This does not approve a production importer, private-source processing or a default extractor.

## Behavior added

The existing [JATS storage proof](SYNTHETIC_JATS_IMPORT_PROOF_2026-11-26.md) now selects among local JATS XML, local HTML and a PDF text-layer path in that order. A candidate records representation kind, origin URL, local path and whether it contains stored bytes or is only a linked URL. A `linked_url`, such as the Catalog Page observed in the owner's Zotero capture, is reported as a link; it is never treated as local HTML bytes.

JATS still requires an article root and matching DOI. HTML requires an `<article>` element, a matching `citation_doi` meta tag and extractable content; a browser-check page fails. The HTML projection records passages, section titles, table text with cell boundaries, figure captions and reference entries with native IDs and deterministic fallback paths. PDF reuses `experiments/extraction_proof.py`'s existing pypdf conversion function, stores the exact PDF bytes in the common representation store, and records page and line locators for text. It does not infer table or figure structure. A PDF without a text layer is held for review rather than accepted as successful extraction.

The selected representation, extractor version and source URL remain bound to stored bytes and segment locators. Search after deleting a fixture source file reads SQLite, not the original file. Failed candidates are not stored. Selection and uncertainty remain explicit through review flags: rejected XML or HTML, link-only HTML, missing local candidate, section fallback, figure/table evidence review, PDF identity uncertainty, PDF structure review and absent PDF text layer.

| Synthetic case | Result |
|---|---|
| Valid XML, HTML and PDF | JATS selected; XML section without native ID gets a path fallback; figure is flagged for visual review |
| Wrong-DOI XML with valid HTML | XML rejected; HTML selected with table and HTML-structure review flags |
| Zotero-style linked HTML plus browser-check HTML and valid PDF | Both HTML candidates skipped; PDF selected with page locator and identity/structure review flags |
| Invalid HTML and invalid PDF bytes | Needs review; no source or representation stored |
| PDF without extractable text | Needs review with `pdf_no_text_layer`; no false text result stored |

Seven focused tests (the earlier two JATS tests plus five route tests) passed. The tests cover exact stored PDF bytes, run reuse, and search after XML, HTML or PDF input files are removed. These are contract checks, not accuracy measurements on arbitrary publisher HTML or PDF layouts.

## Dependency and scope notes

This run reused installed Beautiful Soup 4.14.3, pypdf 6.7.0 and defusedxml 0.7.1; no package was installed. [Beautiful Soup is MIT-licensed](https://www.crummy.com/software/BeautifulSoup/), [pypdf is BSD-3-Clause](https://pypi.org/project/pypdf/) and [defusedxml uses the PSF license](https://pypi.org/project/defusedxml/). [pypdf's security policy](https://github.com/py-pdf/pypdf/security) applies fixes to its latest version; the installed 6.7.0 environment is not a dependency choice for untrusted production PDFs. The bounded tests do not replace a version, security and resource review before adoption.

The HTML parser is intentionally generic and flagged for structural review. It does not claim coverage of publisher-specific HTML, equations, layout tables or all references. The PDF path is plain text only; Docling remains a separate layout path. XML and HTML locators do not establish PDF page numbers. A PDF DOI cannot be proven from its text-layer signature, so the PDF route flags identity for a reviewed source mapping. An exact quoted substring still requires separate claim-support review before becoming a learning object.

## Next gate

Use this interface to compare synthetic PDF text and Docling layout outputs against the same quality rules, then decide whether one shared store can replace the separate experiments. Before connecting authentic Zotero sources to the app, the owner must approve a real-source data policy and implementation boundary. The current synthetic-only application pilot remains unchanged.
