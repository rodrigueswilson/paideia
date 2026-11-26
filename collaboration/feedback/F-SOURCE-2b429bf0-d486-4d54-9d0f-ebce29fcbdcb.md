# Finding: F-SOURCE-2b429bf0-d486-4d54-9d0f-ebce29fcbdcb
- Sender agent/session: Codex / 2026-11-25 independent general review
- Recipient agent/role: Lead editor and owner
- Baseline version/commit: v0.1; SHA-256 `539793ec71de00a10df50cf7e79b4693ab583ccc6398620e607c1be3e3ed8fd2`; no Git commit
- Target document/section/requirement: Sections 6, 8, 13; REQ-03, REQ-04, REQ-13
- Severity: major
- Confidence: high
- Verification status: Verified design ambiguity; no import fixtures inspected
- Related finding/task IDs: T-50e54f71-ee3f-4421-8526-f45c356c41b7

## Finding and rationale
The MVP requires reimport without duplicate identity and an unchanged original, while the model also permits multiple documents per source and version/hash changes. It does not state which identity is stable across reimport, relocation, file replacement, or improved extraction. If a source locator points to a changed extraction, a previously approved quote or question may silently appear grounded in the wrong passage.

## Evidence (URLs, observed tests, or explicit unknowns)
Internal: section 6 lists source/document/segment IDs and version/hash; section 8 stores normalized artifacts and metadata; section 13 requires import twice without duplicate identity and passage location. No migration or locator-stability rule is specified.

## Proposed change and alternatives
Separate work identity, binary document identity, extraction-run identity, and segment version. Define when an import reuses an ID, creates a new version, or is treated as a distinct representation. Bind generated objects to the exact passage/extraction version and require revalidation or a visible stale state after source or parser changes. For the first slice, immutable extracted snapshots are a simple option.

## Implementation impact and acceptance test
Adds identity/version rules and invalidation work. Import the same file twice, move it, replace its content at the same path, and re-extract with a changed parser using authorized fixtures. Verify no duplicate for identical bytes, no silent substitution for changed bytes, and stale status for affected learning objects.
