# Finding: F-ARCH-da783aff-9866-44bb-a25d-2c5d7934fec2
- Sender agent/session: Claude Code (claude-opus-5-5) / T-af8918a8-3a0f-478e-984a-c04053c1fbfd
- Recipient agent/role: Lead editor
- Baseline version/commit: v0.1 frozen; SHA-256 `539793ec71de00a10df50cf7e79b4693ab583ccc6398620e607c1be3e3ed8fd2`; no Git repository
- Target document/section/requirement: Architecture (pipeline, background work, semantic index, Neo4j); Feed orchestration; MVP "no performance thresholds"; REQ-09 (C), Q-05, Q-09
- Severity: moderate
- Confidence: medium
- Verification status: Reasoning from the baseline. The volume figures are the reviewer's estimates and UNVERIFIED. No benchmarks performed.
- Related finding/task IDs: F-ARCH-3814c990-9004-422a-bce5-8b344d509dc3; F-ARCH-50054825-3fc7-46a5-b169-c6ddac34f1ef; F-ARCH-9c681ecc-63cc-4ca2-8779-5b3269e5c85f

## Finding and rationale
The baseline is right to refuse invented thresholds. But it also gives no expected workload size and no measurement plan, so choices like job queues, vector indexes, Neo4j and caching will be made by intuition.

At one learner's scale the plausible workload fits comfortably in one SQLite file queried in-process. My estimate, not a measurement: hundreds to low thousands of documents, tens of thousands of objects and roughly 100,000 events a year. The only heavy work is extraction and LLM generation, and both can run in batches on the host. The risk is premature infrastructure (a message broker, a pool of workers, a graph server) that adds operating burden without benefiting the learner, and LLM costs that grow without limit if content is generated in bulk.

## Evidence (URLs, observed tests, or explicit unknowns)
- Baseline: "Semantic index and Neo4j graph storage deferred until a justified use case; typed relations can initially live in SQLite". REQ-09 confirms a graph *capability*, with Neo4j only as a *candidate*. Also Q-05, and MVP "No performance thresholds invented before fixtures and baseline".
- The volume figures above are the reviewer's estimates and UNVERIFIED.

## Proposed change and alternatives
Recommended:
- Size the expected workload from the audit (counts of Zotero items and attachments, Kindle highlights, Anki cards and reviews). Build a synthetic data generator at 10 times that size.
- Run background work from a jobs table in SQLite, polled by the single backend process (extraction, generation, pack building). No broker. Generate content on demand for each approved passage or session, record tokens and cost on the GenerationRecord, and enforce a daily budget setting.
- Deliver the graph capability (REQ-09) in slice two: a relations table, recursive CTE queries and a client renderer (Cytoscape.js or Mermaid). Adopt Neo4j only if a named query over the 10x fixture misses a target the owner accepts.
- Mobile efficiency: downloading packs and uploading events in batches (F-ARCH-9c681ecc-63cc-4ca2-8779-5b3269e5c85f) bounds network and battery use. Measure it; don't optimize yet.

Alternative: if aggregate queries for Insights become slow, use DuckDB for analytics. It is also embedded and needs no server.

## Implementation impact and acceptance test
Decide now: slice one has a single process, an embedded database and a jobs table, with no broker, graph server or vector database. Defer: semantic search, Neo4j and an analytics engine. Cost of getting it wrong: low if these are deferred, because adapters keep switching cheap; high ongoing operating effort if the infrastructure is adopted early.

Measurements to record, after which the owner sets budgets:
- import latency per page and per document
- extraction CPU and RAM
- FTS query p50/p95 over the 10x fixture
- feed build p95 for a 30-minute session
- core.db growth per 1,000 events
- LLM tokens and cost per approved object
- pack size and bytes uploaded per mobile session
- time for a 3-hop relation query
