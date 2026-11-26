# Finding: F-PRIV-de8fa32f-7f52-4c4b-8f4f-ccdd74d6d2d9
- Sender agent/session: Codex / 2026-11-25 independent general review
- Recipient agent/role: Lead editor and owner
- Baseline version/commit: v0.1; SHA-256 `539793ec71de00a10df50cf7e79b4693ab583ccc6398620e607c1be3e3ed8fd2`; no Git commit
- Target document/section/requirement: Sections 6, 8, 12–13, 16; REQ-08, REQ-12, REQ-13; Q-10/Q-13
- Severity: major
- Confidence: high
- Verification status: Verified ordering gap; no threat model or data audit performed
- Related finding/task IDs: T-50e54f71-ee3f-4421-8526-f45c356c41b7

## Finding and rationale
Learning-event collection is confirmed, but data minimization, retention/deletion, backups, lost-device response, and provider permissions remain proposed or open. The MVP already logs answers and potentially source-linked text. A later privacy decision would require changing event, sync, backup, and export contracts after personal data exists. Privacy choices should be settled before real learner data enters the first slice, even if offline Android sync comes later.

## Evidence (URLs, observed tests, or explicit unknowns)
Internal: REQ-08 is C; section 6 calls for an append-only event stream with later correction/deletion; section 8 requires deletion propagation and device revocation; section 13 calls for “basic privacy controls”; Q-13 leaves retention/deletion and backup policy open. This is a sequencing finding, not a statement that data has leaked.

## Proposed change and alternatives
Make a minimal owner-approved data policy a gate for real use: event fields, free-text limits, local storage locations, retention, deletion semantics, backup copies, export scope, and whether any provider sees source or learner data. Use synthetic fixtures until approved. An alternative is an explicitly disposable prototype that forbids real learner data and has a documented teardown.

## Implementation impact and acceptance test
Requires a small policy and threat-model decision before data-bearing implementation. With a synthetic learner and two device replicas, demonstrate export, deletion, tombstone/reconnect behavior, backup/restore treatment, and lost-device revocation according to the approved policy.
