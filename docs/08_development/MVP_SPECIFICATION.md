# MVP — proposed vertical slice
First prove one complete loop: select authorized PDF -> extract and index -> generate verified quotation and retrieval/comprehension question -> approve -> display responsive feed -> answer -> log event -> change later ranking. Start with a small fixture set and one learner, no cloud required. Anki integration experiment and Android offline sync experiment may run separately before committing architecture.

Acceptance gates:
- Import same document twice without duplicate identity; preserve original unchanged and locate source passage.
- Reject or flag unverifiable quotation and invalid generated schema; answer feedback cites relevant source.
- User can filter topic and complete a timed session; responsive UI usable on phone/tablet widths.
- Every answer creates one durable event, including after retry; a documented rule changes next selection based on evidence.
- Backup/restore and basic privacy controls tested; no secrets or private sources in logs.
- Android milestone separately requires cached learning while host off and duplicate-free event reconciliation after reconnect; validate on actual devices before calling mobile complete.

Deferred: full graph DB, all OCR types, full Anki embedding, comprehensive German syllabus, native Android packaging if not needed for first slice, advanced recommender and speech assessment. Pilot domains proposed: philosophy source-based learning and German structured learning. No performance thresholds invented before fixtures and baseline.
