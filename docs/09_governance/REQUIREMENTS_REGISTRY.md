# Requirements registry
C = owner-confirmed direction; P = proposed design; R = research/decision pending. All acceptance evidence is pending.

| ID | Status | Requirement | Verification target |
|---|---|---|---|
| REQ-01 | C | Personal self-education, name Paideia | Charter review |
| REQ-02 | C | Windows host and Android phone/tablet | Actual device tests |
| REQ-03 | C | Zotero sources and Obsidian notes/Kindle imports | Connector fixtures |
| REQ-04 | C | Document extraction/storage and educational processing | Import-to-object test |
| REQ-05 | C | Anki cards/decks and review integration or reuse | Scheduling authority experiment |
| REQ-06 | C | Mixed learning feed and category/time-based sessions | Session test |
| REQ-07 | C | Language posts and Duolingo-like principles research | Language pilot review |
| REQ-08 | C | Learning event and card data collection | Event integrity test |
| REQ-09 | C | Diagrams and knowledge graph capability, Neo4j candidate | Graph proof of concept |
| REQ-10 | C | Reuse Research MCP and suitable open source | Inventory and license review |
| REQ-11 | C | Multi-agent documentation and feedback | Feedback round trip |
| REQ-12 | P | Offline-first study and synchronization | Host-off and reconnect tests |
| REQ-13 | P | Source provenance, quality gates and safe renderers | Citation/validation tests |
| REQ-14 | P | Local-first, API-first modular architecture | Architecture review |
| REQ-15 | P | Distinguish memory scheduling and pedagogical recommendation | Engine tests |
| REQ-16 | P | German and philosophy pilots | Pilot acceptance |
| REQ-17 | P | Learning effectiveness evaluation beyond engagement | Evaluation protocol |
| REQ-18 | R | Final framework, database, licensing and Anki authority | Decision records |

Traceability: REQ-01 charter; 02/12/14 architecture; 03/05 integrations; 04/06/07/09/15 learning environment and domain model; 08 domain model; 10 reuse policy; 11 collaboration protocol; 13/17 evaluation; 16 language framework and MVP; 18 open questions. Add test IDs after implementation.

## Owner-approved planning constraints, 2026-11-25

- D-011: A synthetic PDF loop is a technical pilot. It does not satisfy the confirmed requirements by itself. A first user-usable release requires a separately approved coverage matrix and acceptance gates. Relevant: REQ-02 through REQ-09, especially REQ-02/03/05/07/09.
- D-012: Anki is the sole grader of Anki-owned cards until disposable-profile tests and a new authority decision. This leaves the integration mechanism open. Relevant: REQ-05/08/15/18.
- D-013: The technical pilot uses synthetic data only. Real learner events or private source material require a later owner-approved data policy and scope. Relevant: REQ-03/04/08/12/13.

These constraints do not change C/P/R classifications or count as acceptance evidence. Proposed milestone coverage remains in `docs/08_development/PHASE0_PILOT_CONTRACTS_DRAFT.md` for later owner review.
