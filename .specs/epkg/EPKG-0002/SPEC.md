---
id: EPKG-0002-SPEC
title: Rocky architecture baseline and engineering asset catalog specification
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0002
issue: BIT-465
---

# EPKG-0002 specification

## Objective and traceability

Create Rocky's first formal, technology-neutral architecture baseline and catalog of engineering
knowledge assets. This package builds on [PRD-001](../../../docs/prd/PRD-001.md) without changing
its accepted foundation or implementing the product domains it defers. It is constrained by
[ADR-001](../../../docs/adr/ADR-001.md), [ADR-002](../../../docs/adr/ADR-002.md), and
[ADR-003](../../../docs/adr/ADR-003.md).

## Deliverables

- ARCH-001 with the system boundary, initial domain model, Knowledge Asset model, bounded-context
  map, logical layers, dependency rule, capability status, constraints, and deferred decisions.
- CAT-001 with canonical locations, lifecycle states, owners, relationships, and maintenance rules.
- A global documentation index and updated root and AI navigation.
- RFC, Pattern, Lesson Learned, and Postmortem templates linked from the template index.
- A complete EPKG-0002 README, SPEC, PROMPT, TESTS, and REVIEW set.
- Glossary additions needed for the new asset types and architecture language.

## Constraints

Write technical documentation in English and use repository-relative links. Link canonical policy
and terminology rather than copying it. Preserve EPKG-0001 and all bootstrap quality gates. Clearly
label implemented, partially implemented, planned, and conceptual capabilities. Treat Artifact as
an architectural hypothesis only. Do not add runtime Artifact or Workspace code, persistence,
integrations, provider code, dependencies, a database choice, or a graph-technology choice. Keep the
change limited to BIT-465.

## Acceptance criteria

1. ARCH-001 exposes an internally consistent system context, Knowledge Asset model, context map,
   logical layers, inward dependency rule, capability status, and explicit deferrals.
2. CAT-001 inventories canonical governing, architecture, package, operational, and template assets
   without duplicating their content or suggesting runtime implementation.
3. Root, documentation, architecture, template, package, and agent navigation reach the new assets,
   and every repository-relative Markdown link resolves.
4. All four templates contain fit-for-purpose metadata, evidence/context sections, consequences or
   follow-up where applicable, and no provider or infrastructure coupling.
5. Source, dependencies, Make targets, CI, EPKG-0001 artifacts, and runtime behavior are unchanged;
   all required checks pass and REVIEW records exact factual results.
6. The complete diff contains no secret, contradiction, accidental placeholder outside templates,
   inaccessible authority, technology selection, or unrelated work.
