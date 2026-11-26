# Finding: F-LEARN-03de0c1c-7a14-4c47-af8d-d3b9e3e2d62c
- Sender agent/session: Codex / 2026-11-25 independent general review
- Recipient agent/role: Lead editor and owner
- Baseline version/commit: v0.1; SHA-256 `539793ec71de00a10df50cf7e79b4693ab583ccc6398620e607c1be3e3ed8fd2`; no Git commit
- Target document/section/requirement: Sections 1, 4, 7, 12–13; REQ-06, REQ-17
- Severity: moderate
- Confidence: high
- Verification status: Verified gap in acceptance criteria; no learning outcomes measured
- Related finding/task IDs: T-50e54f71-ee3f-4421-8526-f45c356c41b7

## Finding and rationale
The first slice passes when an answer changes later ranking, but a change is not evidence of a useful or safe decision. The evaluation section proposes delayed recall and novel application without attaching a predeclared learning or usability gate to the feed rule. A rule could respond to one assisted answer as if it were mastery, or over-prioritize due cards at the expense of coherent reading while still passing the MVP test.

## Evidence (URLs, observed tests, or explicit unknowns)
Internal: section 1 defines success beyond screen time; section 7 proposes several ranking signals and says skip is not a knowledge gap; section 12 distinguishes practice from assessment; section 13 requires a documented rule to change next selection based on evidence, without correctness criteria. No causal efficacy is claimed by this finding.

## Proposed change and alternatives
Specify a tiny scenario suite for the first rule: correct unaided answer, hinted answer, skip, due review, and continuation of a coherent lesson. State expected ranking behavior and user override. Keep delayed assessment as a later evaluation gate with predeclared interval and rubric. Simpler alternative: in the first slice log evidence and show a transparent fixed queue, postponing adaptive ranking until the scenarios are defined.

## Implementation impact and acceptance test
Adds deterministic rule tests and a user-facing explanation; little new infrastructure. Given the scenario suite, the rule must produce the expected next item and rationale, and a skip or assisted answer must not be treated as demonstrated mastery. Later learning claims require delayed assessment evidence, not event counts alone.
