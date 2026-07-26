# Rocky glossary

This file is the canonical vocabulary for Rocky artifacts. Other documents link here rather than
redefining these terms.

| Term | Definition |
| --- | --- |
| **Rocky Engineering Framework (REF)** | The policies, artifacts, and validation practices that make engineering intent and evidence repository-native. |
| **Product Charter (RKY)** | The durable statement of product mission, principles, boundaries, and measures. |
| **Product Requirement Document (PRD)** | A testable definition of a product problem and desired outcomes, independent of implementation. |
| **Architecture Decision Record (ADR)** | An immutable-after-acceptance record of one consequential architecture decision and its trade-offs. |
| **Engineering Package (EPKG)** | A bounded, reviewable unit containing a specification, execution prompt, review record, and validation plan. |
| **Specification (SPEC)** | The normative scope, constraints, deliverables, and acceptance criteria for an EPKG. |
| **Prompt (PROMPT)** | Provider-neutral execution guidance derived from a SPEC; it is not a substitute for the SPEC. |
| **Review (REVIEW)** | Recorded evidence that an EPKG satisfies product, architecture, documentation, and quality expectations. |
| **Test Plan (TESTS)** | The verification strategy and commands that demonstrate acceptance criteria. |
| **Repository as Knowledge** | The practice of storing canonical, versioned engineering context beside the code it governs. |
| **Agent** | A human-directed automation role with explicit responsibilities and boundaries. |
| **Knowledge Asset** | A repository-managed unit of engineering knowledge with a stable identity, lifecycle metadata, accountable ownership, relationships, and reviewable content. |
| **Engineering Domain** | A bounded, technology-independent model of governed engineering concepts, policies, and behavior. Its implementation does not own repository governance and remains independent from infrastructure; [ADR-004](adr/ADR-004.md) governs the architectural boundary. |
| **Engagement** | The engineering work context approved for specification by [PRD-002](prd/PRD-002.md); it is not implemented. |
| **Artifact** | A conceptual future domain entity representing a structured unit of engineering knowledge; it is an architectural hypothesis and not an implemented runtime type. |
| **Bounded Context** | An explicit semantic boundary within which a model and its vocabulary are consistent. |
| **Engineering Asset Catalog (CAT)** | The inventory of canonical engineering knowledge assets, their locations, lifecycle states, owners, and relationships. |
| **System Architecture (ARCH)** | A technology-neutral baseline describing system boundaries, capability status, contexts, logical layers, and dependency rules. |
| **Request for Comments (RFC)** | A time-bounded proposal used to gather review before a consequential approach is adopted. |
| **Pattern** | A reusable, context-specific engineering solution with forces, consequences, and known limits. |
| **Lesson Learned** | A concise record of observed experience and an actionable improvement. |
| **Postmortem** | A blameless record of an incident's impact, timeline, contributing conditions, response, and follow-up actions. |
