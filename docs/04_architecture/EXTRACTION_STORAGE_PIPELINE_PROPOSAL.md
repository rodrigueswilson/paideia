# Persistent extraction and retrieval pipeline — proposal

Status: design proposal for Paideia, 2026-11-25. It does not approve Docling, a database migration, real-source access, or a change to the frozen v0.1 specification. The technical pilot remains synthetic-only under D-013.

## Why this comes before object generation

The master architecture already specifies source → extraction/quality → normalized segments → search/retrieval → generation/validation. The current synthetic pilot stores PDF bytes, extracted full text, its hash, extractor label, and approved objects in SQLite. It proves persistence, but it has no general segment table, structured table/figure representation, retrieval index, extraction-run comparison, or stale-object reconciliation. Expanding generation before those contracts would bind learning objects to ad hoc text offsets and make later re-extraction costly.

The recommended next technical slice is therefore **ingest once, retrieve many times**. A conversion job should be repeatable and idempotent; study and generation should query stored, versioned passages without running PDF conversion each time.

## Proposed flow

```text
Authorized source reference
  → document identity (bytes hash; original remains authoritative)
  → extraction job (engine + exact version + settings + schema version)
  → immutable structured extraction artifact and quality report
  → normalized, addressable segments and SQLite FTS index
  → retrieval by source, topic/filter, passage and locator
  → draft learning objects with exact segment/extraction references
  → separate validation and human approval
```

The first experiment uses only synthetic PDFs. Later connector work must use a disposable library or explicitly authorized copies and must not write to Zotero, Obsidian, Kindle, Anki, or Research MCP production data.

## Storage contract to test

| Record | Minimum stored fields | Authority and update rule |
|---|---|---|
| Source | Stable Paideia ID, title, source type, external system/library/item ID | Bibliographic authority remains external; Paideia stores a reference. |
| Document | Content hash, source link, original locator, format, observed version/time | Original remains in its authoritative repository. A changed byte hash is a new document version; do not overwrite history. |
| ExtractionRun | Document hash, engine, exact version, configuration hash, output schema version, started/completed time, quality/error status | Derived and immutable. Repeated identical runs can reuse an artifact; changing engine/settings creates a new run. |
| ExtractionArtifact | Full structured conversion output and its hash | Derived, rebuildable. Initially store JSON in SQLite if size is acceptable; measure whether large artifacts belong in an ignored content-addressed file store with a database pointer. Never put private artifacts in Git. |
| Segment | Extraction ID, stable-within-run ID/order, type, text, heading/context, page and bounding box where available, text hash, quality flag | Queryable projection from one extraction run. Do not assume segment IDs survive re-extraction. |
| Search index | Segment text and IDs in SQLite FTS5 | Rebuildable projection; no vector database required for the first retrieval proof. |
| LearningObject citation | Segment ID, extraction ID, quoted text/context, validation state | Object remains bound to the exact extraction used for approval. A new extraction triggers revalidation or visible stale status, never silent retargeting. |

Use constraints and foreign keys so deleting or replacing a derived projection cannot silently remove an approved object's evidence. Define an explicit archival or revalidation path before any extraction purge. Store authored annotations and learner events separately from rebuildable extraction data.

## Docling's role and alternatives

Docling is a strong **candidate extractor** because its current `DoclingDocument` API can export a structured dictionary/JSON representation, and its model includes text, table and provenance items. Its [documentation](https://docling-project.github.io/docling/v2/) describes exporting and reloading the document as JSON. Its [serialization guide](https://docling-project.github.io/docling/concepts/serialization/) notes that Markdown flattens merged table cells, so the full structured export is preferable when table fidelity matters. These are documented capabilities, not evidence that Docling is the best or fastest extractor on the owner's PDFs.

Define one `Extractor` contract returning the structured artifact, normalized segments, locators, quality report and exact engine metadata. Compare:

- `pypdf` text-layer path already used by the synthetic pilot: small dependency and adequate for simple text-layer fixtures, with limited layout structure.
- Research MCP's existing PDF path: potential internal reuse, but its inspected processor/cache files were untracked and the cache's item-key identity is insufficient as Paideia's provenance authority.
- Docling: evaluate structure, tables, reading order and OCR behavior on representative authorized material; record version, model assets, licenses, install size, latency, memory and failure modes before adoption.

Select Docling as the default only if the measured source mix benefits enough to justify its cost. It may instead be a second-stage extractor for complex pages or a fallback after a text-layer quality check. The Paideia database contract should not depend on a Docling-only field.

## Bounded proof and acceptance evidence

1. Build or use several *synthetic* PDFs covering plain text, two columns, a table, a scan/OCR case, and changed document bytes. Keep expected passages and locators as fixture truth.
2. Run each candidate in an isolated environment and persist immutable extraction runs. Record extraction time, peak memory, install footprint, passage recall/fidelity, reading order, table structure and missing/uncertain text. No production source is needed for this first comparison.
3. Import identical bytes twice. Confirm one document identity and no duplicate extraction for identical engine/version/settings; changing any of these creates a separate run.
4. Query stored segments after restarting the app with conversion disabled. Confirm the relevant passage, source reference, page/locator and extraction version return without parsing the PDF again.
5. Change bytes and re-extract. Approved objects tied to the prior run must remain traceable and be marked stale or revalidated explicitly. A quotation that does not match its cited extraction cannot be approved.
6. Back up and restore the database plus any external derived artifact store; verify the same retrieval results and citation links. Measure size before choosing a one-store versus split-store design.

## Decision after the proof

The owner/lead can then approve an exact extractor version and strategy, the artifact storage layout, and the next generation scope. Until then, Docling remains a candidate. Draft learning-object generation should consume only approved, stored segments with explicit provenance; it should never retrieve an unversioned blob and invent a citation.
