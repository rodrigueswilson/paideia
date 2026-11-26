# Finding: F-ARCH-a5ad9adf-ccf1-4e7e-ab75-42473d4f1de6
- Sender agent/session: Claude Code (claude-opus-5-5) / T-af8918a8-3a0f-478e-984a-c04053c1fbfd
- Recipient agent/role: Lead editor; owner for the authority rule
- Baseline version/commit: v0.1 frozen; SHA-256 `539793ec71de00a10df50cf7e79b4693ab583ccc6398620e607c1be3e3ed8fd2`; no Git repository
- Target document/section/requirement: Learning environment (Feed, Memory); Integrations/Anki; Cross-device; REQ-05, REQ-06, REQ-15, D-006
- Severity: major (close to critical: a wrong choice corrupts a long-lived review history)
- Confidence: high
- Verification status: Reasoning from the baseline. External claims are marked VERIFIED (primary doc fetched 2026-11-25) or UNVERIFIED. No tests performed.
- Related finding/task IDs: F-ARCH-9c681ecc-63cc-4ca2-8779-5b3269e5c85f

## Finding and rationale
The baseline wants one authoritative scheduler ("Do not grade a card in two schedulers") and also a mixed Feed that includes cards and ranks by review urgency. On Android, Anki's scheduler is AnkiDroid, a separate app with its own collection and sync. Suppose Paideia's feed shows an Anki-scheduled card and records an answer. Either Paideia grades it, which makes it a second scheduler and the histories diverge, or the answer is a non-grading event that the learner still experiences as a review. The second case is double exposure: it distorts Anki's intervals and Paideia's evidence alike. The four-way experiment (AnkiConnect, embedded core, FSRS, fork) is framed as a choice of mechanism. The decision that actually drives rework is which system owns each item, and that rule can be fixed now whatever the mechanism.

## Evidence (URLs, observed tests, or explicit unknowns)
- Baseline: Memory "one authoritative scheduler"; Feed object types include flashcards/cards; Integrations "scheduler authority until explicit migration"; Cross-device "no offline grading promise until verified".
- VERIFIED: AnkiDroid offers an Instant-Add API (a wrapper over a ContentProvider, needs the READ_WRITE_DATABASE permission) that lets third-party apps add notes (https://github.com/ankidroid/Anki-Android/wiki/AnkiDroid-API). It supports pushing notes into Anki, not grading from outside it.
- UNVERIFIED (the page fetch failed): AnkiConnect is a desktop add-on that serves HTTP on localhost:8765 and needs Anki desktop running (https://ankiweb.net/shared/info/2055492159). If true, it cannot serve Android or work while the host is off.

## Proposed change and alternatives
Recommended, and simplest: separate scheduling domains.
1. An item scheduled by Anki is graded only in Anki or AnkiDroid. Paideia never presents it as a gradeable card. The feed may show "N due in Anki" with a deep link.
2. Paideia pushes approved card-type objects one way into Anki: an .apkg export or AnkiConnect on the host first, the AnkiDroid API later. It keeps an ExternalReference from Paideia object id + version to Anki note id.
3. Paideia imports Anki review logs read-only, as events with source=anki, deduplicated by Anki review id, for Insights and ranking.
4. Paideia-native objects (open questions, comprehension, language exercises) use Paideia's own scheduler, rule-based or FSRS. Each item lives in exactly one domain, recorded on the object.

Alternative A: Paideia becomes the only scheduler (FSRS), and Anki is frozen or migrated after a backup. This is larger in scope, gives up AnkiDroid, and is the owner's decision.
Alternative B: in slice one Paideia only reads Anki and pushes nothing; cards are written by hand in Anki.

## Implementation impact and acceptance test
Decide now: the separate-domain rule, and that Paideia never grades Anki items (owner). Defer: the push mechanism, FSRS adoption, the AnkiDroid integration. Cost of getting it wrong: corrupted or duplicated review history in a long-lived Anki collection, which is hard to undo.

Test, on a disposable Anki profile only: push 20 synthetic notes. Review 10 on desktop and 5 on AnkiDroid, then sync. Import the review logs into Paideia twice. Pass if there are exactly 15 Anki events, Paideia recorded zero grades on those notes, and re-pushing an edited object updates its note instead of duplicating it.
