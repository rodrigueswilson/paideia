# Decision log
| ID | State | Decision / rationale |
|---|---|---|
| D-001 | Confirmed | Paideia — Personal Learning System; self-education |
| D-002 | Confirmed | Independent project on owner's G drive; Windows and Android phone/tablet |
| D-003 | Confirmed | Kindle via existing Obsidian import; Zotero and Anki existing; reuse Research MCP |
| D-004 | Confirmed | Investigate open-source reuse including Anki; independent agent feedback |
| D-005 | Proposed | Local-first API and SQLite initial store, Neo4j later |
| D-006 | Proposed | Anki authority preserved until integration/migration experiment |
| D-007 | Proposed | Responsive UI first; native framework after comparative test |
| D-008 | Proposed | German and philosophy pilots, bounded vertical slice |
| D-009 | Proposed | Read-only discovery, sanitized reviews, owner approval gates |
| D-010 | Proposed | File-based agent collaboration with Git branches and immutable findings |
| D-011 | Confirmed | Synthetic PDF loop is a technical pilot, not completion of confirmed requirements; first user-usable release is defined separately |
| D-012 | Confirmed | Anki-owned cards are graded only in Anki pending disposable-profile tests and a separate authority decision |
| D-013 | Confirmed | Technical pilot uses synthetic data only until a real learner-data policy is approved |
| D-014 | Confirmed | Approve bounded implementation of the synthetic PDF-to-question-to-answer technical pilot |
| D-015 | Confirmed | Use local Git and publish a sanitized public GitHub repository |

For future decisions record ID, status, date, approver, context, alternatives, evidence, consequence, affected requirements and superseded decision. Do not rewrite history.

## D-011 — technical pilot boundary
- Status/date/approver: Confirmed, 2026-11-25, owner.
- Context: The proposed PDF-to-question loop does not cover every confirmed integration, Android, language, or graph objective.
- Alternatives considered: Call the loop the first user-usable release; require all confirmed integration boundaries in the first loop; or name it a technical pilot with separate release coverage. The owner approved the third option.
- Evidence: Two review submissions, provisional synthesis, and the proposed coverage matrix; no product or device tests.
- Consequence: Pilot success cannot be reported as fulfillment of all confirmed requirements. A first user-usable release must receive its own scope and acceptance gates. This decision does not approve product implementation.
- Affected requirements: REQ-02 through REQ-09 and REQ-11, especially REQ-02/03/05/07/09.
- Superseded decision: None. This narrows interpretation of proposed D-008, which remains proposed.

## D-012 — interim Anki scheduling authority
- Status/date/approver: Confirmed, 2026-11-25, owner.
- Context: A mixed feed and card events risk duplicate grading while Anki integration and migration mechanisms remain unresolved.
- Alternatives considered: Paideia grades Anki-owned cards; immediate migration to a Paideia scheduler; or Anki alone grades Anki-owned cards pending tests. The owner approved the third option.
- Evidence: Review findings and existing integration specification; no Anki API, profile, or Android experiment yet.
- Consequence: Paideia must not grade an Anki-owned card in the technical pilot or any later workflow under this interim rule. Paideia-native questions may have their own events. Push/import mechanisms, mapping, migration, and any change of authority require separate evidence and decision.
- Affected requirements: REQ-05, REQ-08, REQ-15, REQ-18.
- Superseded decision: None. Refines proposed D-006 without approving a mechanism.

## D-013 — synthetic-only technical pilot
- Status/date/approver: Confirmed, 2026-11-25, owner.
- Context: Event collection is confirmed, while retention, deletion, backups, exports, and external-processing permissions are not yet approved for real learner data.
- Alternatives considered: Collect real data under an interim policy; or limit the technical pilot to synthetic data until a policy is approved. The owner approved the second option.
- Evidence: Review findings and the open privacy questions; no data audit or threat-model test.
- Consequence: Pilot fixtures and events must be synthetic. Real learner or private source data require a later owner-approved data policy and scope. This does not choose retention periods, backup destination, provider access, or deletion design.
- Affected requirements: REQ-03, REQ-04, REQ-08, REQ-12, REQ-13.
- Superseded decision: None. The broader privacy questions remain open.

## D-014 — bounded technical-pilot implementation scope
- Status/date/approver: Confirmed, 2026-11-25, owner.
- Context: Phase 0 prohibited product implementation without an approved scope change. The owner accepted the recommended synthetic technical pilot as the next implementation step.
- Alternatives considered: Continue documentation only; implement the full confirmed product scope immediately; or build one bounded synthetic PDF-to-question-to-answer loop. The owner approved the bounded loop.
- Evidence: D-011/012/013, review synthesis, draft pilot contracts and acceptance scenarios. No product test evidence yet.
- Consequence: Product code may be created for synthetic PDF import/extraction, passage and question approval, responsive session display, answer events and transparent next selection. Code should be small and measurable. No production collection connection, real learner data, Anki grading, general offline sync, graph database, or claim of a user-usable release is authorized. Candidate framework and dependency choices still require their own evidence.
- Affected requirements: REQ-04/06/08, with preparatory interfaces for REQ-02/03/05/13.
- Superseded decision: None; this is the explicit scope change required by the Phase 0 rule.

## D-015 — local Git and public GitHub repository
- Status/date/approver: Confirmed, 2026-11-25, owner.
- Context: The local repository had no commits; the owner requested local Git and a public GitHub repository.
- Alternatives considered: Remain local only; use a private remote; or publish a sanitized public remote. The owner approved the public remote.
- Evidence: Owner instruction and pre-publication file review. No repository publication is claimed by this decision record alone.
- Consequence: Commit and publish only reviewed nonprivate files. Keep local setup notes, credentials, databases and private source/learner material ignored. A public repository does not resolve the open source license decision.
- Affected requirements: REQ-10/11/18 and governance of all public project files.
- Superseded decision: None.
