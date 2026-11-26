# Integration contracts — pending local audit
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
