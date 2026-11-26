# Research MCP read-only reuse inventory — 2026-11-25

Status: preliminary code inspection for Paideia Phase 0. This summary contains no machine-local paths, credentials, or source material. It is not an integration test, security audit, license determination, or dependency adoption decision.

## Observed structure and constraints

- Research MCP has a coordinator, a Zotero local provider, a PDF processor provider, extraction utilities, a hybrid cache, and corresponding unit-test files. The coordinator registry constructs the Zotero and PDF providers. The code was inspected without importing or executing it.
- Its working tree contains many pre-existing changes. The Zotero local provider and coordinator service are tracked, while the PDF processor provider, PDF extractor, hybrid cache, and their examined tests are currently untracked. A clean commit cannot reproduce the full apparent runtime. No Research MCP file was changed.
- `pyproject.toml` declares Python 3.12+ and a broad dependency set. The lockfile records, among others, pdfplumber 0.11.8, Docling 2.61.1, EasyOCR 1.7.2, torch 2.9.0, diskcache 5.6.3, and requests 2.32.5. These are observed lockfile versions, not adopted Paideia dependencies. No install size or performance measurement was taken.
- No project-root license file was found in this inspection. Component-specific license files may exist. Ownership and distribution terms require clarification before code copying or packaging.

## Reuse classification

| Capability | Observed evidence | Preliminary classification | Gate before use |
|---|---|---|---|
| Zotero metadata and attachment lookup | Tracked `zotero_local` client/provider exposes list, search, item, annotation, and attachment-path methods; it also exposes write methods. Mock-based tests exist. | Candidate for a narrow read-only adapter or reference. | Verify the local API and attachment mapping using a disposable profile or authorized copy; enforce a read-only interface and check error/identity behavior. |
| PDF text extraction | Untracked PDF provider and extractor use pdfplumber with optional OCR and structure processing. Tests exist but were not run. | Reference or candidate for adaptation after reproducible snapshot. | Compare a minimal text-layer extractor with this path on authorized fixtures; measure fidelity, latency, memory, and dependency footprint. |
| Coordinator service | Large service imports extraction, cache, cost, and orchestration modules and has broad responsibilities. | Reference; avoid direct dependency for the first Paideia slice. | Isolate a small API contract only if a proof shows reuse is cheaper than a narrow adapter. |
| Hybrid extraction cache and FTS | Untracked `HybridCache` creates directories and SQLite tables on construction, stores extracted text by item key, and invalidates mainly from file modification time when a path is supplied. The coordinator's cache lookup can occur without that path. | Do not reuse directly as Paideia's provenance store. | Rework identity around document/extraction version and test stale-cache behavior on changed bytes; decide whether a cache is needed at all. |
| Search and research workflows | Methods and documentation exist for search, citation work, and other research tasks. | Reference only for now. | Demonstrate a Paideia-specific need and inspect that bounded module, its tests, dependencies, and license. |

## Implications for Paideia

The confirmed reuse requirement calls for testing existing components, not importing the whole runtime. The first useful experiment is a read-only Zotero adapter against a disposable fixture, followed by a PDF extraction comparison. Keep Paideia's source identity, passage provenance, learning objects, and events under its own explicit contract. Do not treat Research MCP's item-key cache as a source of truth for approved quotations.

## Evidence and limits

Inspected `pyproject.toml`, `uv.lock`, `src/coordinator/{registry,service,app}.py`, `src/providers/zotero_local/{client,config,provider}.py`, `src/providers/pdf_processor/{config,provider}.py`, `src/utils/{pdf_extractor,hybrid_cache}.py`, and related test file names and test declarations. Checked tracked/untracked status for these paths. No tests, network calls, application imports, credential reads, local collection reads, benchmarks, or dependency/license audits were performed.
