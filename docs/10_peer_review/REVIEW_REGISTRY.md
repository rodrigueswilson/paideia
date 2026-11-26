# Review registry
Record review ID, model/version, role, baseline hash, received date, finding IDs, verification status and synthesis link. Keep raw feedback in collaboration/feedback or private/ if it contains sensitive information. Independent reviews remain isolated until submission.

| Review ID | Model/version and role | Baseline | Received | Findings | Verification | Synthesis |
|---|---|---|---|---|---|---|
| R-2026-11-25-CODEX | Codex (exact model version unavailable), independent general review | v0.1, SHA-256 `539793ec71de00a10df50cf7e79b4693ab583ccc6398620e607c1be3e3ed8fd2` | 2026-11-25 | Seven `F-SCOPE`, `F-ANKI`, `F-PROV`, `F-EVENT`, `F-SOURCE`, `F-PRIV`, `F-LEARN` records in `collaboration/feedback/` | Internal baseline review only; no external claims or empirical tests verified | `collaboration/synthesis/S-8de42c0d-a8b6-4d09-9e25-f809541c693c.md` |
| R-2026-11-25-CLAUDE-ARCH | Claude Code (claude-opus-5-5), architecture/efficiency review | Same frozen v0.1 hash | 2026-11-25 | Seven `F-ARCH` records in `collaboration/feedback/` | Mixed verified and unverified external claims per records; no device, integration, or benchmark tests. Partial exposure to the earlier reviewer's handoff is disclosed in its handoff. | Same synthesis |

Neither review is an approved decision. The synthesis contains provisional recommended dispositions only.
