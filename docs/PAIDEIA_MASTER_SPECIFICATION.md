# Paideia — Personal Learning System

Master specification v0.1 | 2026-11-25 | Frozen draft for independent review

This is a generated consolidation of modular documents. Owner-confirmed directions are labeled C in the requirements registry; other designs are proposals. No local audit, code implementation or independent evidence verification completed. Local machine paths and private data are deliberately omitted. The Windows host, Android clients, existing Zotero/Obsidian/Kindle/Anki ecosystem and German study are relevant project context.

---

Section 1 | Source document: `00_foundation/PROJECT_CHARTER.md`

## Project charter
Status: v0.1; owner-confirmed purpose and name, proposed design principles.

Paideia is a personal learning system for continuous self-education, supporting acquisition, comprehension, retention, integration and application of knowledge. Education is intellectual formation rather than mere accumulation. The name and subtitle, Windows host, Android phone and tablet clients, existing source ecosystem, feed, language practice and learning data collection are owner requirements. Open-source reuse and multi-agent review are owner-directed strategies.

Design principles: learning over engagement; understanding over consumption; retention over accumulation; integration over fragmentation; evidence over intuition; autonomy over dependence; epistemic integrity over convenience. No engagement-maximizing dark patterns. Make recommendations explainable and overridable.

Non-goals for the first release: commercial platform, public social network, wholesale replacement of Zotero or Obsidian, unrestricted automated code generation, scientifically validated mastery inference, all languages, all document types, or a full Anki fork. These are scope proposals, not permanent exclusions.

Success: a useful, reproducible end-to-end learning cycle with traceable sources and recorded evidence, followed by evaluation of delayed recall, comprehension and transfer rather than screen time alone.

---

Section 2 | Source document: `00_foundation/GLOSSARY.md`

## Glossary
- Source: bibliographic or intellectual work; document: a particular digital representation; segment: addressable passage with extraction provenance.
- Learning object: reusable instructional unit; micro-lesson: coherent sequence of objects; session: bounded goal-directed study; pathway: progressive objectives and prerequisites.
- Claim: proposition with evidence and attribution; concept: conceptual entity; relation: typed, provenance-bearing connection, not necessarily a fact.
- Learning event: observation of interaction; learner state: uncertain inference from observations; mastery: criterion-dependent performance, not directly observed knowledge.
- Memory scheduler: determines when to review; pedagogical recommender: selects what to do next; orchestration: coordinates scheduler, curriculum and learner goals.
- Authority: designated system of record; replica: synchronized copy; provenance: traceable origin and transformation history.
- Review baseline: immutable version supplied to independent reviewers; finding: actionable criticism; disposition: reasoned decision on a finding.

---

Section 3 | Source document: `09_governance/REQUIREMENTS_REGISTRY.md`

## Requirements registry
C = owner-confirmed direction; P = proposed design; R = research/decision pending. All acceptance evidence is pending.

| ID | Status | Requirement | Verification target |
|---|---|---|---|
| REQ-01 | C | Personal self-education, name Paideia | Charter review |
| REQ-02 | C | Windows host and Android phone/tablet | Actual device tests |
| REQ-03 | C | Zotero sources and Obsidian notes/Kindle imports | Connector fixtures |
| REQ-04 | C | Document extraction/storage and educational processing | Import-to-object test |
| REQ-05 | C | Anki cards/decks and review integration or reuse | Scheduling authority experiment |
| REQ-06 | C | Mixed learning feed and category/time-based sessions | Session test |
| REQ-07 | C | Language posts and Duolingo-like principles research | Language pilot review |
| REQ-08 | C | Learning event and card data collection | Event integrity test |
| REQ-09 | C | Diagrams and knowledge graph capability, Neo4j candidate | Graph proof of concept |
| REQ-10 | C | Reuse Research MCP and suitable open source | Inventory and license review |
| REQ-11 | C | Multi-agent documentation and feedback | Feedback round trip |
| REQ-12 | P | Offline-first study and synchronization | Host-off and reconnect tests |
| REQ-13 | P | Source provenance, quality gates and safe renderers | Citation/validation tests |
| REQ-14 | P | Local-first, API-first modular architecture | Architecture review |
| REQ-15 | P | Distinguish memory scheduling and pedagogical recommendation | Engine tests |
| REQ-16 | P | German and philosophy pilots | Pilot acceptance |
| REQ-17 | P | Learning effectiveness evaluation beyond engagement | Evaluation protocol |
| REQ-18 | R | Final framework, database, licensing and Anki authority | Decision records |

Traceability: REQ-01 charter; 02/12/14 architecture; 03/05 integrations; 04/06/07/09/15 learning environment and domain model; 08 domain model; 10 reuse policy; 11 collaboration protocol; 13/17 evaluation; 16 language framework and MVP; 18 open questions. Add test IDs after implementation.

---

Section 4 | Source document: `01_pedagogy/PEDAGOGICAL_FRAMEWORK.md`

## Pedagogical framework — proposed
Retrieval practice, spacing, elaboration, interleaving, generative learning, scaffolding, multimedia learning, metacognition, transfer and self-regulated learning are research candidates. Do not treat them as universally effective regardless of task or learner. Translate evidence into testable design rules, noting boundary conditions and population differences.

| Mechanism | Proposed design | Evaluation |
|---|---|---|
| Retrieval | Answer before reveal; corrective feedback | Delayed unaided recall |
| Spacing | Schedule appropriate repeated retrieval | Retention at defined intervals |
| Comprehension | Explain, compare, reconstruct arguments | Rubric-scored novel questions |
| Scaffolding | Prior knowledge checks and optional hints | Independent performance after support |
| Transfer | Novel cases, varied contexts | Application beyond practiced items |
| Metacognition | Confidence before feedback | Calibration against outcomes |
| Multimedia | Meaningful diagrams paired with text | Comprehension, not viewing time |

Pre-reading: activate prior knowledge, introduce vocabulary and guiding questions without replacing the original reading. During reading: contextual explanations, annotations and source navigation. Post-reading: recall, analysis, application and spaced review.

### Microlearning
Short objects are delivery units, not proof of learning. Group related objects into micro-lessons, sessions and pathways; support deep reading and context restoration. Proposed durations: micro-lesson 3–10 minutes, session 10–60 minutes; user-adjustable, not evidence-based thresholds. Use optional goals, progress and reminders, not punitive streaks, leaderboards or endless engagement loops.

### Research agenda
Prioritize systematic reviews and meta-analyses of adult learning, retrieval, spacing, reading comprehension, cognitive load, corrective feedback, SLA, CALL/MALL, microlearning, self-regulation and transfer; then knowledge tracing, adaptive sequencing and educational recommenders. Record search terms, databases, inclusion criteria, study populations, effect uncertainty, limitations and design implications. Verify publisher/DOI records and distinguish independent research from vendor claims. No systematic review completed.

---

Section 5 | Source document: `01_pedagogy/LANGUAGE_LEARNING_FRAMEWORK.md`

## Languages — proposed pilot
German is the initial candidate because the owner studies it with Duolingo. Keep schemas multilingual; support Portuguese/English glosses and eventually Spanish/French and other languages. CEFR descriptors may structure goals but do not supply a complete syllabus, vocabulary list or proficiency certification.

Separate receptive and productive vocabulary, morphology, syntax, grammar, reading, listening, speaking, writing, pronunciation and pragmatic competence. Lexical records should include lemma, sense, language, part of speech, inflections, example, collocations, source and verification state; German nouns additionally gender and plural. Separate performance estimates per skill.

Pilot exercises: article/gender, plural, case, conjugation, word order, cloze, matching, sentence construction and contextual translation. Support audio later after validating quality and licenses. Accept legitimate alternate answers; avoid one rigid translation key. Example: Ich helfe den Mann -> Ich helfe dem Mann; record observed case mismatch, not a definitive diagnosis of ignorance. Repeated errors may motivate targeted practice and reassessment.

Study Duolingo's public principles (progression, short interactive lessons, corrective feedback, adaptive practice) without copying proprietary content, branding or code. Evaluate Lute for authentic reading, LibreLingo/community alternatives for lesson schemas, Anki/FSRS for retention and open grammar tools. Prefer independently licensed German material. No assumption of importing Duolingo account data.

---

Section 6 | Source document: `02_conceptual_models/DOMAIN_MODEL.md`

## Conceptual model — not a database schema
Source -> Document -> Segment -> Claim/Concept/Argument -> Objective -> LearningObject -> Event -> LearnerState -> Recommendation.

| Entity | Key attributes and relationships |
|---|---|
| Source, Document, Segment | Stable IDs, bibliographic identity, version/hash, source locators, extraction engine and quality; one source may have multiple documents |
| Annotation | Author, kind, original locator, exact text or comment, timestamp; distinguish quoted author from learner |
| Concept, Claim, Relation | Typed links, aliases, language, evidence, confidence, review state; many-to-many |
| Objective, Pathway | Observable competency, prerequisites, success criterion; sequence is revisable |
| LearningObject | Type, content schema/version, objective IDs, source links, difficulty estimate, answer/rubric, validation, generation provenance |
| Session, Event | Session goal, device, object version, timestamp, outcome, assistance and confidence where appropriate |
| LearnerState | Skill/concept dimension, estimate, uncertainty, evidence IDs and estimator version |
| ExternalReference | System, external identifier, mapping and synchronization version |
| GenerationRecord, ValidationRecord | Model/prompt version, inputs, timestamp, checks, reviewer and disposition |

Taxonomies: subject, language, skill, cognitive objective, object type, difficulty, source type and review status. Multiple classifications allowed. Typed graph edges distinguish support, contradiction, implication, historical influence, association and prerequisite; Obsidian links are associations unless independently substantiated.

Event envelope proposed: event_id UUID, device_id, session_id, object_id, object_version, event_type, occurred_at UTC, received_at, schema_version, payload. Capture presented, answered, revealed, skipped, hint_requested, confidence_rated, session_completed. Store attempts separately from inferred mastery; minimize sensitive free text. Append-only by default with explicit correction/deletion mechanisms and privacy retention policy.

---

Section 7 | Source document: `03_functional_specifications/LEARNING_ENVIRONMENT.md`

## Learning environment — proposed specifications

| Area | Function |
|---|---|
| Library | Select and search sources, see provenance, import status and extraction warnings |
| Reader | Open original passage, navigate PDF/EPUB where supported, display explanations |
| Studio | Generate, edit, validate and approve objects; separate generated content from quotations |
| Feed | Mixed stream of quotes, excerpts, explanations, diagrams, questions, cards and language practice; filter topic, difficulty, objective; explain why shown |
| Memory | Review cards using one authoritative scheduler; inspect due items and feedback |
| Study | Time-bounded goal such as German for 30 minutes; estimate activity durations, allow stop/skip/extend |
| Languages | Structured competencies, error-focused practice and authentic text reading |
| Knowledge | Explore source-backed concepts, relationships and argument maps |
| Pathways | Prerequisite-aware progression alongside exploratory study |
| Insights | Review history, delayed performance, confidence calibration and coverage; do not equate clicks with knowledge |

Initial object types: verified quote, excerpt, explanation, open retrieval question, multiple choice, cloze, flashcard; later diagrams, matching, argument maps, timelines, writing, listening and application tasks. Use schema-validated content and trusted renderers rather than arbitrary AI code. Every generated object has a source or explicitly labeled external/AI origin, version, answer or rubric when applicable, and validation state. Quotation exact-match checks must account for documented extraction normalization; uncertain OCR is flagged.

Feed orchestration: filter eligible content by selected goal, due status, validated content and offline availability; rank by review urgency, relevance, prerequisite gaps, novelty, difficulty and diversity. Include coherent lesson sequences and user control. Log rationale, ranking version and outcome. Begin rule-based, not engagement optimization or opaque machine learning. Keep memory scheduler separate from curriculum selection. A skipped item is not automatically a knowledge gap or dislike.

---

Section 8 | Source document: `04_architecture/SYSTEM_ARCHITECTURE.md`

## Architecture — candidate, not approved implementation
Local-first modular monolith on Windows, backend API separated from clients. Candidate Python/FastAPI, React/TypeScript responsive UI, SQLAlchemy/Alembic, SQLite/FTS5 and filesystem. Android phone/tablet support is required; responsive PWA then Capacitor or React Native is a proposed path, to compare with ePoc reuse, Flutter and native Android. Evaluate existing app foundation versus greenfield.

Sources -> connector adapters -> extraction/quality checks -> normalized segments -> search/retrieval -> generation/validation -> learning object store -> feed/session planner -> clients -> event ingestion -> learner model -> recommendations.

Keep originals in their authoritative repositories; store normalized artifacts and metadata with hashes. Docling candidate primary extraction, PyMuPDF/pdfplumber fallback, Tesseract for OCR; benchmark on representative authorized samples, including scanned and complex layouts. Semantic index and Neo4j graph storage deferred until a justified use case; typed relations can initially live in SQLite. No duplicate source-of-truth stores. LLM provider adapter, model/prompt versioning, constrained output schemas, citations/locators, explicit opt-in for external processing; no credentials in client or logs.

### Cross-device and offline
Windows owns central Paideia data initially. Android caches selected content and queues events while offline, including when PC is off. Proposed protocol: versioned API, unique event IDs, idempotent uploads, per-device cursors, content versions, acknowledgments and retries. Track occurred and received times; handle clock skew. Append-only observations merge by ID; mutable content uses optimistic concurrency and explicit conflict policy. Deletion/tombstones and retention must propagate. Do not sync a live SQLite file through cloud drive. Test interrupted sync, duplicate submission, conflicting edits and stale objects. Anki reviews need distinct authority and deduplication; no offline grading promise until verified.

Connectivity options: LAN, private authenticated network, optional cloud/hybrid later. Live processing requires host availability unless a separate service is approved. Offline cached study remains possible. TLS/authentication, least privilege, encrypted transport, device revocation, scoped exports, backups and restore tests. Threat model includes malicious documents, prompt injection, untrusted HTML/card templates and lost devices. Never expose unauthenticated backend to the Internet.

---

Section 9 | Source document: `05_integrations/INTEGRATIONS.md`

## Integration contracts — pending local audit
| System | Authority / proposed contract | Unknowns |
|---|---|---|
| Zotero | Bibliographic metadata and original attachments; read-only import initially | Active directory, API availability, attachment mapping |
| Obsidian | Personal Markdown notes, tags, links and Kindle imports; read-only | Vault conventions, plugin format, duplicates |
| Kindle | Existing Obsidian plugin is the ingestion route for highlights/comments | Export completeness, locators, sync format; no DRM bypass |
| Anki | Existing collection and review history; scheduler authority until explicit migration | Integration vs embedded core vs FSRS; Android review semantics |
| Calibre | Optional conversion/ebook source | Installed capabilities, formats and licensing |
| Research MCP | Reuse existing code/concepts after audit; no production changes | Modules, tests, dependencies and provenance |
| Paideia | Generated objects, events, learner estimates, categories and orchestration | Final schemas and retention policies |

Anki decision experiment: compare external API/AnkiConnect, embedded core, independent FSRS and fork. Use disposable collections only. Test note/card/deck mapping, template/media rendering safety, scheduling and review export, undo, sync conflicts and Android compatibility. Independent FSRS is not automatically Anki-compatible. Do not grade a card in two schedulers. Owner decides whether existing Anki remains authoritative or a migration occurs after backup/restore testing.

---

Section 10 | Source document: `06_open_source/REUSE_POLICY.md`

## Open-source reuse policy
Reuse internal components first, then maintained libraries, documented APIs, justified adaptations, forks, and only then custom implementations. Compare adoption of a whole existing platform with composing libraries. Prefer dependency pinning over vendoring. Keep adapters replaceable and record origin, version/commit, exact license, notices, changes, dependencies, security, platform fit, integration cost and maintenance cost. Test critical capabilities using fixtures before selection. No source copying before license/provenance assessment. Preserve option of future distribution; personal use does not remove all licensing concerns. No final Paideia license selected.

Candidate evaluation: score functional fit, maturity, docs/tests, Windows/Android and offline support, privacy, maintenance, accessibility, performance, compatibility and exit cost. Explicitly record blockers and alternative designs. Licensing is version/component specific; verify upstream license text and transitive dependencies; obtain legal advice if distribution requires it.

---

Section 11 | Source document: `06_open_source/COMPONENT_REGISTRY.md`

## Candidate registry — no dependencies adopted
URLs are research starting points carried forward from planning; current availability, license and maintenance not independently rechecked for this release.

| Candidate | Upstream | Evaluation |
|---|---|---|
| Anki core | https://github.com/ankitects/anki | Embedded vs external; AGPL implications |
| AnkiDroid | https://github.com/ankidroid/Anki-Android | Android reference; GPL/component terms |
| FSRS | https://github.com/open-spaced-repetition/py-fsrs | Independent scheduling; compatibility experiment |
| HLR | https://github.com/duolingo/halflife-regression | Historical research baseline, not current Duolingo |
| ePoc | https://epoc.inria.fr/en/ | Offline mobile renderer, content schema or platform foundation |
| H5P | https://h5p.org/ | Interactive exercise renderer, offline, event hooks, per-library terms |
| Docling | https://github.com/docling-project/docling | Extraction benchmark, model licenses |
| PyMuPDF | https://github.com/pymupdf/PyMuPDF | PDF fallback, AGPL/commercial considerations |
| pdfplumber | https://github.com/jsvine/pdfplumber | Tables and extraction |
| Tesseract | https://github.com/tesseract-ocr/tesseract | OCR |
| PDF.js | https://github.com/mozilla/pdf.js | Embedded reader |
| EPUB.js | https://github.com/futurepress/epub.js | EPUB renderer |
| Open Notebook | https://github.com/lfnovo/open-notebook | Source-grounded AI workflow |
| Lute | https://github.com/LuteOrg/lute-v3 | Language reading/lexical tracking |
| LibreLingo | https://github.com/kantord/LibreLingo | Course formats; check maintained forks |
| LanguageTool | https://github.com/languagetool-org/languagetool | Grammar feedback |
| spaCy/Stanza | https://github.com/explosion/spaCy ; https://github.com/stanfordnlp/stanza | Linguistic analysis |
| Neo4j | https://github.com/neo4j/neo4j | Graph persistence later |
| Cytoscape.js | https://github.com/cytoscape/cytoscape.js | Graph visualization |
| Mermaid | https://github.com/mermaid-js/mermaid | Diagrams |
| Oppia | https://github.com/oppia/oppia | Instructional sequences reference |
| Calibre/Pandoc | https://github.com/kovidgoyal/calibre ; https://github.com/jgm/pandoc | Conversion |

Secondary candidates: OCRmyPDF, EbookLib, Moodle, Open edX, Graphviz, Excalidraw, Markmap, React Flow, Whisper, eSpeak NG, LlamaIndex, Haystack, Ollama, LiteLLM, DuckDB, River and ECharts. Do not introduce without a concrete requirement.

Adoption record fields: candidate ID, exact URL, checked date, version/commit, license file and exceptions, proof-of-concept results, security and dependency review, alternatives, integration/exit costs, disposition, decision ID.

---

Section 12 | Source document: `07_evaluation/EVALUATION_PROTOCOL.md`

## Evaluation — proposed
Technical: reproducible import and extraction, traceable quotations, schema validation, safe rendering, duplicate-free events, offline sync recovery, backup restore, accessibility on phone/tablet and desktop. Use synthetic or authorized fixtures; report failures and limitations.

Content: compare generated claims to source passages, check answer ambiguity and alternate answers, rubric alignment, difficulty, attribution and accessibility. Human review sampled by type and risk; high-risk or unsupported content withheld. LLM graders are fallible and must not be sole ground truth.

Learning: baseline performance, immediate and delayed retrieval, comprehension, novel application, calibration and time cost. Define intervals and scoring rubrics in advance, separate practice items from assessment items, avoid conflating repeated item familiarity with transfer. Single-learner longitudinal observations may guide personal improvement but do not establish causal efficacy; stronger designs need counterbalancing/comparators, confound controls and ethical review if research extends beyond personal use. Engagement is secondary.

---

Section 13 | Source document: `08_development/MVP_SPECIFICATION.md`

## MVP — proposed vertical slice
First prove one complete loop: select authorized PDF -> extract and index -> generate verified quotation and retrieval/comprehension question -> approve -> display responsive feed -> answer -> log event -> change later ranking. Start with a small fixture set and one learner, no cloud required. Anki integration experiment and Android offline sync experiment may run separately before committing architecture.

Acceptance gates:
- Import same document twice without duplicate identity; preserve original unchanged and locate source passage.
- Reject or flag unverifiable quotation and invalid generated schema; answer feedback cites relevant source.
- User can filter topic and complete a timed session; responsive UI usable on phone/tablet widths.
- Every answer creates one durable event, including after retry; a documented rule changes next selection based on evidence.
- Backup/restore and basic privacy controls tested; no secrets or private sources in logs.
- Android milestone separately requires cached learning while host off and duplicate-free event reconciliation after reconnect; validate on actual devices before calling mobile complete.

Deferred: full graph DB, all OCR types, full Anki embedding, comprehensive German syllabus, native Android packaging if not needed for first slice, advanced recommender and speech assessment. Pilot domains proposed: philosophy source-based learning and German structured learning. No performance thresholds invented before fixtures and baseline.

---

Section 14 | Source document: `08_development/DEVELOPMENT_ROADMAP.md`

## Roadmap
0. Freeze foundation v0.1; initialize local repository; independent review and synthesis.
1. Read-only infrastructure audit and reuse inventory; parallel evidence and open-source investigation.
2. Resolve architectural decisions using bounded proofs of concept (Anki, mobile/offline, H5P/ePoc, extraction); refine conceptual models and privacy rules.
3. Approve minimum vertical slice and contracts; implement only authorized scope.
4. Expand responsive learning environment, timed sessions and basic analytics; validate source grounding.
5. Android phone/tablet offline learning and sync; validate actual devices and Anki authority.
6. German pilot, pathways, error model and richer exercises; philosophy pilot.
7. Graph exploration and more adaptive recommendations when data and evidence justify them.
8. Evaluate delayed learning outcomes and iterate.

Scientific and technical work proceed in parallel. Each milestone requires acceptance evidence and owner-approved scope. Documentation versions v0.2 after review, v0.3 after audit, later versions after component and pedagogical evaluation; version numbers illustrative, not fixed schedule.

---

Section 15 | Source document: `09_governance/DECISION_LOG.md`

## Decision log
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

For future decisions record ID, status, date, approver, context, alternatives, evidence, consequence, affected requirements and superseded decision. Do not rewrite history.

---

Section 16 | Source document: `09_governance/OPEN_QUESTIONS.md`

## Open questions and risk register
| ID | Question / risk | Resolution |
|---|---|---|
| Q-01 | Active Zotero location, Kindle plugin output, reusable Research MCP modules unknown | Local read-only audit |
| Q-02 | Greenfield vs existing foundation (ePoc/H5P/Open Notebook) | Compare bounded prototypes |
| Q-03 | Anki integration vs embedded core vs FSRS; duplicate grading | Disposable collection tests and licensing |
| Q-04 | Mobile framework and offline sync conflict semantics | Android proof of concept |
| Q-05 | SQLite sufficient? Neo4j timing? | Benchmark actual workload and graph queries |
| Q-06 | Source extraction and AI errors | Representative fixtures and human validation |
| Q-07 | Curriculum scope, German resources and legitimate answers | SLA review and licensed content audit |
| Q-08 | Learner model overinterprets behavior | Separate evidence from inference, uncertainty and delayed tests |
| Q-09 | Scope creep and excessive dependency burden | Vertical slice and adoption gates |
| Q-10 | Personal content leakage, malicious imports, lost devices | Threat model, redaction, authorization and revocation |
| Q-11 | Licensing and future distribution | Exact license audit; owner distribution decision |
| Q-12 | Agent conflicts, hallucinated consensus or prompt injection | Immutable findings, review isolation, verification and owner gates |
| Q-13 | Retention/deletion, backup and remote access policy | Owner privacy decision and restore/sync tests |

---

Section 17 | Source document: `09_governance/AI_COLLABORATION_PROTOCOL.md`

## Multi-agent collaboration protocol v0.1
The initial collaboration feature is a durable file-based inbox/outbox in the repository, not a running agent service. Agents can leave addressed feedback, respond, claim tasks and hand off context without being online simultaneously. It works across models capable of reading/writing files, or by manually importing their responses. No automatic agent invocation, messaging or monitoring is implemented.

### Roles and authority
Owner approves objectives, confirmed requirement changes, privacy and implementation scope. Lead editor integrates decisions and verifies evidence. Specialist agents investigate bounded tasks; independent reviewers challenge frozen baselines. Codex performs local authorized audits and implementation. Agents may recommend, not approve their own changes. If role unknown, default reviewer.

### Workflow
1. Read AGENTS, baseline, requirements, decision log, status and relevant handoffs. Independent reviewers see only frozen review packet before submitting.
2. Create a task record with unique ID, agent/session ID, scope, base commit/version, allowed writes and state. Coordinate ownership through lead; Git branch/worktree is preferred. No distributed lock is implied by file creation.
3. Write a finding to collaboration/feedback/<unique-id>.md using template. Include sender, recipient role or agent, target path/section, baseline, severity, evidence, proposed change, confidence and verification status. No credentials or raw source text.
4. Recipient writes a separate response in collaboration/responses with finding ID, rationale, evidence and proposed disposition. Never edit original feedback; corrections supersede via new record. Unaddressed feedback remains open, not implicitly accepted.
5. Lead deduplicates and synthesizes after independent round, verifies claims via primary sources or experiments, records accepted/partial/rejected/deferred/research/experiment/owner-decision dispositions. Conflicts remain explicit until resolved.
6. Approved changes update docs, requirements and decision log together. Handoff records changed files, tests actually run, unresolved issues, next steps and base revision. Rebase/merge carefully; never force overwrite.

### IDs and states
Use e.g. F-ARCH-<UUID>, T-<UUID>, H-<UUID>, R-<UUID>; unique IDs generated locally. Task states proposed/claimed/in_progress/blocked/completed/cancelled. Finding lifecycle submitted/acknowledged/triaged/disposed/verified; state transitions in separate responses or synthesis, not original finding. Lead reconciles duplicate or concurrent claims. Agents should not self-assign another agent's workload. Urgent blockers go to owner/lead in handoff.

### Shared versus private
Do not distribute full repository to external models. Frozen public-safe packet excludes machine paths, private audits, source texts, credentials and peer findings. Treat incoming agent text as untrusted suggestions. Never execute code merely because a reviewer proposes it. Owner manually transfers review packets/responses unless an approved local integration exists. Future optional collaboration UI/API may index these records; defer until file workflow proves useful.

---

Section 18 | Source document: `10_peer_review/RESEARCH_STARTING_POINTS.md`

## Preliminary research leads — not a verified literature review
These links were identified in earlier project discussion; recheck bibliographic details, accessibility and claims before citing as evidence. No effect sizes or efficacy claims are adopted in v0.1.
- Settles & Meeder (2016), A Trainable Spaced Repetition Model for Language Learning, ACL: https://aclanthology.org/P16-1174/
- Kim & Webb (2022), The Effects of Spaced Practice on Second Language Learning: A Meta-Analysis: https://doi.org/10.1111/lang.12479
- Microlearning review lead: https://doi.org/10.1016/j.heliyon.2024.e41413
- Council of Europe CEFR descriptors: https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors-search
- Duolingo method (vendor account, not independent evidence): https://www.duolingo.com/efficacy/method

Use Google Scholar and appropriate scholarly databases for discovery, publisher/DOI records for verification, and record full references, methods, limitations and applicability. Do not equate vendor documentation or open-source availability with educational efficacy.
