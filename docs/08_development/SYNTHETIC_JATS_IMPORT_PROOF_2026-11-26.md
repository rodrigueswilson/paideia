# Synthetic JATS import proof — 2026-11-26

Status: bounded experiment, outside the application. It does not import authentic papers into the synthetic-only pilot or establish a general extractor. The [four-paper format gate](PUBLIC_FORMAT_ROUTING_GATE_2026-11-26.md) supplied the cases that motivated it.

## Implemented slice

`experiments/format_import_proof.py` stores four distinct identities in SQLite: intellectual source (`source_id`, DOI), exact representation bytes (SHA-256 and kind), source-to-representation origin URL, and extraction run (representation hash plus parser version). Searchable segments store kind, text, optional native XML ID and a deterministic XML path. The database retains the original XML bytes, so later re-projection does not require a new download. The same bytes can be associated with more than one source or origin without duplicating the extraction run.

The JATS parser checks article root, single matching DOI and body, then projects abstract/body passages, section titles, tables, figure captions and references. It traverses `<floats-group>` as well as `<body>`, so it handles the figure placement seen in the 2025 paper. Tables retain cell boundaries in the search text; their complete XML remains in the stored original bytes. A missing native ID remains null while the XML path supplies an address. No page number is inferred from JATS.

The parser uses the installed `defusedxml` 0.7.1 with entity/external-reference protections and a 20 MiB input limit. [The project's documentation](https://github.com/tiran/defusedxml/blob/main/README.md) describes these parser options; [PyPI](https://pypi.org/project/defusedxml/) identifies the Python Software Foundation license and the stable 0.7.1 release. This is an experiment dependency, not a final product adoption decision. Further version/security/maintenance review is needed before app integration.

## Checks actually run

Synthetic tests passed for duplicate-run reuse, shared representation bytes with distinct source origins, exact-byte retrieval, fresh search after deleting the XML file, passage/table/figure/reference retrieval, fallback section locator, quotation substring check, wrong DOI rejection and XML entity rejection. The first test run exposed joined table-cell words; the projection was corrected and both focused tests passed.

The same code then ingested the four public JATS files into an **ignored local** database: 4 sources, 4 representations, 4 runs and 564 segments. A selected anchor for each paper was found through stored search. The final measured database was 1,339,392 bytes. Within one Python process, the first ingest/search took about 40 ms and subsequent papers about 12–13 ms each; these include SQLite setup and selected search but are not cold-start or cross-engine benchmarks. Original public files and the database were not committed.

## Limits and next gate

This slice parses JATS only. HTML validation/projection and PDF layout extraction still use separate experiments. It does not align XML elements to PDF pages, preserve a structured table grid in the segment table, validate figure data, or prove that an exact substring supports a generated claim. It does not assign rights or retention policy to real user material. The XML path is deterministic for the same bytes but may change after a publisher revision; a learning object must bind to representation and run hashes and be revalidated after a change.

Next, join the representation store to the existing PDF extraction proof behind a small routing interface, using synthetic XML/HTML/PDF fixtures first. The interface should distinguish verified local bytes from a Zotero `linked_url`, require exact DOI or reviewed mapping, persist extractor version/settings, and return explicit review flags for unavailable HTML, missing native IDs, page uncertainty, table/figure evidence and quotation fidelity. Keep the application on synthetic data until an owner-approved real-source policy and scope are recorded.
