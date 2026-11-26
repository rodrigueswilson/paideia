# Finding: F-SCOPE-2b1a2b46-b8da-4f4f-9fe2-d6d0668b35f7
- Sender agent/session: Codex / 2026-11-25 independent general review
- Recipient agent/role: Lead editor and owner
- Baseline version/commit: v0.1; SHA-256 `539793ec71de00a10df50cf7e79b4693ab583ccc6398620e607c1be3e3ed8fd2`; no Git commit
- Target document/section/requirement: Sections 3, 8, 13–14; REQ-02, 03, 05, 07, 09
- Severity: major
- Confidence: high
- Verification status: Verified against the frozen baseline only; no implementation evidence
- Related finding/task IDs: T-50e54f71-ee3f-4421-8526-f45c356c41b7

## Finding and rationale
The proposed MVP proves a PDF-to-question feed loop, while confirmed owner requirements include Android phone/tablet, existing integrations, language posts, and graph/diagram capability. The roadmap defers several of these, which may be sensible, but it does not define the release at which each confirmed capability becomes necessary. “First release,” “MVP,” “vertical slice,” and “mobile complete” can therefore be interpreted differently. An MVP success could be mistaken for satisfaction of confirmed scope.

## Evidence (URLs, observed tests, or explicit unknowns)
Internal: REQ-02/03/05/07/09 are C; section 13 defers Android sync, full Anki embedding, German syllabus, and graph DB; section 14 places Android and German pilots in later phases. This is a scope/acceptance ambiguity, not a claim that deferral violates owner intent. No device or integration tests have been run.

## Proposed change and alternatives
Add a release coverage matrix mapping every C requirement to a named milestone, minimal proof, acceptance gate, and owner decision if any part is deferred. Define whether the PDF loop is a technical pilot or a user-usable first release. A simpler alternative is to call it a prototype explicitly and reserve “MVP” for the first milestone covering the owner’s minimum usable workflow.

## Implementation impact and acceptance test
Documentation and planning only. Given each C requirement, a reviewer can identify its first required milestone, test evidence, and explicit owner-approved deferral if it is absent from a proposed release.
