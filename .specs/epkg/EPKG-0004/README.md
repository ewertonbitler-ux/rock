---
id: EPKG-0004
title: Engagement Core Domain
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
---

# EPKG-0004: Engagement Core Domain

This package specifies Rocky's first governed Engineering Domain runtime model. It implements the
accepted [PRD-002](../../../docs/prd/PRD-002.md) through a persistence-free `Engagement` aggregate
that protects ownership, participation, lifecycle, decisions, and milestones while preserving the
inward dependency rule in [ARCH-001](../../../docs/architecture/ARCH-001.md).

Read package artifacts in this order:

1. [SPEC](SPEC.md) — normative domain boundary, behavior, and acceptance criteria.
2. [PROMPT](PROMPT.md) — provider-neutral implementation procedure.
3. [TESTS](TESTS.md) — required automated and manual verification.
4. [REVIEW](REVIEW.md) — review checklist and evidence record.

Persistence, APIs, delivery tools, external providers, messaging, AI orchestration, and repository
integration remain outside this package.