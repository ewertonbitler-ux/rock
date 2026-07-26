---
id: EPKG-0004-PROMPT
title: Engagement Core Domain execution guidance
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0004
---

# EPKG-0004 execution guidance

Implement EPKG-0004 from a clean or understood checkout. Read
[PRD-002](../../../docs/prd/PRD-002.md), [ARCH-001](../../../docs/architecture/ARCH-001.md), the
accepted ADRs, and this package in README, SPEC, PROMPT, TESTS, REVIEW order.

The [SPEC](SPEC.md) is normative. When repository authority conflicts with this package, stop and
record the conflict rather than inventing requirements.

## Execution contract

- Implement only the persistence-free Engagement domain and explicitly justified tests.
- Preserve the aggregate boundary and lifecycle matrix exactly.
- Keep external identities as neutral actor references; do not add provider lookups.
- Do not add repositories, application services, persistence, APIs, frameworks, adapters, events,
  integrations, AI orchestration, or speculative abstractions.
- Use typed domain failures and read-only collection exposure.
- Make the smallest coherent change and preserve unrelated repository work.
- Run every command in [TESTS](TESTS.md) and record exact evidence in [REVIEW](REVIEW.md).
- Inspect the complete diff and verify every new relative Markdown link.
- Do not mark the package accepted, merge the pull request, or claim release without maintainer
  action.