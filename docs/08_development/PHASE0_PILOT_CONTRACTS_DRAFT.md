# Phase 0 pilot contracts and coverage — draft for owner review

Status: proposal based on the frozen v0.1 baseline and the provisional review synthesis. This is a planning artifact, not an approved architecture or implementation scope. All test data below are synthetic or explicitly authorized copies.

Owner-approved boundaries on 2026-11-25: D-011 confirms the synthetic PDF loop is a technical pilot separate from the first user-usable release; D-012 keeps Anki as sole grader of Anki-owned cards pending disposable-profile tests; D-013 limits the technical pilot to synthetic data. The detailed identities, event schema, validation design, milestone coverage and acceptance scenarios below remain proposals.

## Milestone meanings

- **Phase 0:** documentation, synthesis, read-only code discovery, and fixture/test plans. No product code.
- **Technical pilot (proposed):** a synthetic PDF-to-question-to-event loop that tests contracts and learning usability. It cannot be called the first complete release.
- **Integration proofs (proposed):** separate disposable-fixture experiments across Zotero, Obsidian/Kindle, Anki, and Android.
- **First user-usable release:** owner-defined coverage of confirmed requirements, with actual-device and authorized-data evidence. Its boundary is an open owner decision.

## Confirmed requirement coverage

| Requirement | Earliest proposed proof | Required evidence before declaring the requirement met |
|---|---|---|
| REQ-01 Personal self-education and name | Phase 0 charter and pilot framing | Owner confirms intended workflow and naming. |
| REQ-02 Windows and Android phone/tablet | Online responsive test during integration proofs | Actual phone and tablet task completion; offline behavior only if approved for the release. |
| REQ-03 Zotero, Obsidian and Kindle imports | Separate read-only connector fixtures | Stable source mapping, annotation attribution, duplicate import and changed-source handling on authorized samples. |
| REQ-04 Document extraction/storage and educational processing | Technical pilot | Passage locator, extraction provenance, quote validation, generated question approval, and stale status after re-extraction. |
| REQ-05 Anki integration or reuse | Disposable Anki proof | One scheduling authority; note/card mapping, safe review-log handling, retry and Android implications. No production writes in discovery. |
| REQ-06 Mixed feed and category/time sessions | Technical pilot, expanded in usable release | Topic filter, timed session, coherent sequence, explainable selection and user override. |
| REQ-07 Language posts and Duolingo-like principles research | Language research and later German pilot | Licensed content, legitimate alternate answers and skill-specific evaluation. Public principles are research leads, not copied content. |
| REQ-08 Learning event and card data collection | Synthetic technical pilot | Durable logical attempts across retries, provenance and correction/deletion rules; real use gated on owner data policy. |
| REQ-09 Diagrams and knowledge graph capability | Bounded relation/renderer proof after pilot | A source-backed diagram or relation workflow that meets a user task; Neo4j is not required unless measured need justifies it. |
| REQ-10 Reuse Research MCP and suitable open source | Phase 0 preliminary inventory, then fixture proofs | Reuse/adapt/reference decisions with reproducible snapshot, exact versions/licenses, cost and behavior evidence. |
| REQ-11 Multi-agent documentation and feedback | Phase 0 file workflow | Submitted findings, separate responses and dispositions, traceable handoff. Automation is not required. |

**Open owner decision:** Which of the integration proofs must be completed before the first user-usable release, and which may arrive in named later releases? A confirmed requirement is never silently removed by this matrix.

## Minimum contracts to settle before pilot implementation

1. **Source and extraction identity.** Give each intellectual source a stable internal ID; store external system/library/item references separately. Identify original document bytes with a cryptographic hash, allowing one source to have several document versions and shared bytes to have several source references. Identify each extraction by document hash, extractor version and settings. A learning object cites a specific extraction and passage anchor. Re-extraction must either re-resolve the anchor with evidence or mark the object stale; it must never silently retarget it. Test quote/context and position hints before fixing an anchor format.
2. **Content validation.** Record separate states for quotation fidelity, extraction confidence, claim support, answer/rubric adequacy and alternate-answer review. A source link alone does not imply support. The initial pilot may use manual approval of a small set instead of automated claim verification.
3. **Attempt and event identity.** A presentation has a stable ID; one logical answer attempt has an attempt ID; observations have event IDs. A lost acknowledgment reuses the same IDs. A deliberate second attempt gets a new attempt ID. Correction or deletion is explicit and linked to the affected record. Preserve object version and both occurred/received times. Define the storage transaction that makes an accepted attempt durable exactly once.
4. **Scheduler authority.** Every reviewable item has one scheduling domain. Anki-owned items are graded only in Anki until the owner chooses another arrangement after disposable-profile tests. Paideia-native questions may record Paideia attempts. The push/import method and any Paideia scheduler are still open.
5. **Data authority and lifecycle.** Label each record as externally authoritative, Paideia-owned or rebuildable derived data. Keep the technical pilot synthetic. Before real learner data, the owner approves field minimization, retention, deletion, backups, exports and external processing. A physical split into two stores is not required by this classification.

## Proposed technical-pilot acceptance sheet

| Scenario | Pass evidence |
|---|---|
| Import identical PDF twice | One document-byte identity, stable source mapping, no duplicate approved object. |
| Replace bytes or change extractor | New document/extraction version; affected object flagged or revalidated, never silently retargeted. |
| Valid and altered quotation | Valid quote resolves to a passage; altered quote is rejected or held for review. |
| Unsupported inference and ambiguous answer | Distinct validation failure states; unresolved question is withheld from learner feed. |
| Answer, lost acknowledgment, repeat upload, second attempt | One stored logical attempt for retry; second deliberate attempt remains distinct; links and versions preserved after restart. |
| Correct unaided answer, hinted answer, skip, lesson continuation | Documented rule selects and explains the next item; assistance or skip is not counted as demonstrated mastery. |
| Desktop, phone and tablet widths | Core session is usable at each width. Online browser testing does not establish offline Android support. |
| Backup and restore with synthetic data | Owned events and approved objects survive restore; derived views can be rebuilt or documented as intentionally preserved. |
| Resource baseline | Record import time, extraction CPU/RAM, feed response time, database growth and any generation cost. Set targets after representative fixtures. |

No criterion above claims educational efficacy. Delayed recall, comprehension and transfer require a separately planned evaluation with predeclared items, intervals and rubrics.
