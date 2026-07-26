---
id: EPKG-0001-SPEC
title: Rocky Engineering Framework foundation specification
status: accepted
version: 1.0.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0001
---

# EPKG-0001 specification

## Objective and traceability

Establish a production-quality, navigable foundation satisfying all requirements in
[PRD-001](../../../docs/prd/PRD-001.md). The design is constrained by
[ADR-001](../../../docs/adr/ADR-001.md), [ADR-002](../../../docs/adr/ADR-002.md), and
[ADR-003](../../../docs/adr/ADR-003.md).

## Deliverables

- RKY-000 charter, PRD-001 definition, REF-001 handbook, and ADR-001 through ADR-003.
- Provider-neutral `.ai` context and role catalog.
- A complete EPKG-0001 set: README, SPEC, PROMPT, REVIEW, and TESTS.
- Reusable ADR, PRD, and EPKG templates plus review and release checklists.
- Root navigation and a minimal Python 3.11 bootstrap with lint, type-check, tests, and local-link validation.

## Constraints

Use English and official [glossary](../../../docs/glossary.md) terms. Keep metadata aligned at
version `1.0.0` and date `2026-07-26`. Link to canonical policy rather than repeat it. Do not add
future product domain classes, hosted services, vendor-specific AI integrations, secrets, or
unrelated automation.

## Acceptance criteria

1. Every PRD-001 requirement maps to a deliverable and review evidence.
2. Root and index navigation reach every canonical artifact, and all relative Markdown links resolve.
3. Templates enforce required metadata, traceability, context, decision/scope, consequences, and validation.
4. The bootstrap installs with its development extra and all four documented quality gates pass.
5. Final review finds no contradiction, unnecessary duplication, unfinished placeholder, inaccessible context dependency, or unrelated change.
