# Phase 0 decision sheet — proposed, 2026-11-25

This sheet turns two independent-review submissions into choices for the owner. It is not a decision log entry and does not change any confirmed requirement, privacy boundary, or implementation scope. The frozen v0.1 baseline remains the reference. See the synthesis in `collaboration/synthesis/` and the Research MCP inventory in `docs/08_development/`.

## Owner approval recorded 2026-11-25

The owner approved the three recommended boundaries below. They are now confirmed decisions D-011, D-012, and D-013 in the decision log. This sheet retains the original recommendations for context. The owner did not approve a product implementation scope, integration mechanism, real-data policy, or exact first user-usable release coverage.

## Recommended decisions

| Decision | Recommended choice | Why now | Evidence still needed |
|---|---|---|---|
| Scope of the first loop | Name the synthetic PDF-to-question loop a **technical pilot**. Name a later milestone the **first user-usable release**, with explicit coverage of each C requirement. | Prevents a narrow pilot from being counted as completion of owner goals. | Owner's minimum usable workflow and requirement-to-milestone matrix. |
| Anki scheduling | For the pilot, an Anki-owned card is graded only in Anki. Paideia-native questions can produce Paideia events. Do not migrate or write to an existing collection. | Card identity and event semantics depend on authority. | Disposable-profile test of note IDs, review logs, retries, editing, and Android behavior. |
| Learner data | Keep the pilot synthetic until a minimal real-data policy is approved. | Retention, deletion, backups, and provider access shape the event contract. | Owner choices for retention, deletion, backup location, and external processing. |

## Work to complete within Phase 0

1. Lead writes final finding dispositions after owner decisions and checks the overlap disclosure. Keep originals intact.
2. Create the requirement-to-milestone coverage matrix, including Android phone/tablet, Zotero/Obsidian/Kindle, Anki, language posts, and graph/diagram capability. Distinguish a capability from a candidate technology such as Neo4j.
3. Specify the minimum contracts: source/document/extraction identity; passage anchors and stale status; validation by content type; logical attempt IDs and retry/correction semantics; scheduler domain; owned versus rebuildable data.
4. Use synthetic fixtures for a read-only Research MCP Zotero adapter check and a small extraction comparison. Clarify code reproducibility and licensing before adoption. No production collection access or code copying is implied.
5. Prepare a pilot acceptance sheet covering quotation fidelity, ambiguous answers, duplicate import, stale extraction, retries, coherent feed selection, backup/restore, and phone/tablet widths. Measure latency and resource use before setting budgets.

## Proposed implementation gate

The owner reviews the contracts, audit results, and pilot acceptance sheet, then explicitly approves a bounded product-implementation scope. A likely pilot is one host process, one embedded store, a responsive UI, and synthetic content. Zotero, Kindle/Obsidian, Anki, and offline Android are separate bounded experiments; their results determine the first user-usable release. No framework, database, extractor, or packaging choice is approved here.
