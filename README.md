# Paideia — Personal Learning System
Foundation release v0.1 | 2026-11-25 | Draft for independent review

Paideia supports lifelong self-education through source-grounded learning, durable retention, conceptual understanding and skill development. Inspired by the Greek ideal of paideia and Werner Jaeger's work, it is intended for one learner initially, across Windows and Android.

## Start here
- [Master specification](docs/PAIDEIA_MASTER_SPECIFICATION.md): public-safe conceptual review baseline.
- [Project charter](docs/00_foundation/PROJECT_CHARTER.md) and [requirements](docs/09_governance/REQUIREMENTS_REGISTRY.md): authority and scope.
- [AGENTS.md](AGENTS.md): instructions for every collaborating agent.
- [Agent collaboration](docs/09_governance/AI_COLLABORATION_PROTOCOL.md): durable feedback and handoffs.
- [Review protocol](docs/10_peer_review/REVIEW_PROTOCOL.md) and [review prompts](docs/10_peer_review/REVIEW_PROMPTS.md).
- [Roadmap](docs/08_development/DEVELOPMENT_ROADMAP.md), [MVP](docs/08_development/MVP_SPECIFICATION.md), [status](docs/08_development/PROJECT_STATUS.md).
- [Local initialization](LOCAL_START.md): private, owner/Codex only.

## Status
The frozen v0.1 master specification is an independent-review baseline. Two reviews and a provisional synthesis are recorded; the decision log includes owner approval for a bounded synthetic technical pilot. A preliminary read-only Research MCP code inventory exists. The pilot uses no production integrations and provides no empirical learning validation. Confirmed owner requirements remain distinct from proposed designs and research candidates. Do not interpret the pilot approval as authorization to modify existing collections.

## Run the synthetic technical pilot

Requires Python 3.12 or newer. In PowerShell from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m paideia_pilot.server
```

Open `http://127.0.0.1:8766`. Import the bundled synthetic PDF, inspect and approve its three fixture-authored questions, then start a timed session. Answers are self-rated without saving typed text. The server binds to loopback only, and its SQLite data is under ignored `data/`.

Run the focused checks with `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`. The pilot does not import arbitrary PDFs, connect to Zotero/Obsidian/Kindle/Anki, grade Anki cards, or provide Android offline access. Its [PDF dependency decision](docs/06_open_source/ADOPTION_PYPDF_PILOT.md) is limited to this synthetic fixture.

For external reviewers, send the separate review packet, not the full repository. It excludes local paths and agent working records. All AI outputs are proposals until reviewed; multiple agreeing models are not independent empirical evidence.

## License
The project license has not been selected. See REQ-18 and the decision log before reusing or distributing project code.
