# Conceptual model — not a database schema
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
