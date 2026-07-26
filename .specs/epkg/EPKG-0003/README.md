---
id: EPKG-0003
title: Knowledge Asset Core Domain
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
issue: BIT-466
preparation_issue: BIT-470
---

# EPKG-0003: Knowledge Asset Core Domain

This proposed package makes BIT-466 implementation-ready. It introduces Rocky's first runtime
aggregate, `KnowledgeAsset`, within the inward dependency rule of
[ARCH-001](../../../docs/architecture/ARCH-001.md). `Artifact` remains an architectural hypothesis
and is not part of the runtime model. The package is constrained by
[ADR-001](../../../docs/adr/ADR-001.md), [ADR-002](../../../docs/adr/ADR-002.md), and
[ADR-003](../../../docs/adr/ADR-003.md).

Read package artifacts in this order:

1. [SPEC](SPEC.md) — normative BIT-466 boundary, behavior, and acceptance criteria.
2. [PROMPT](PROMPT.md) — provider-neutral implementation procedure.
3. [TESTS](TESTS.md) — required automated and manual verification.
4. [REVIEW](REVIEW.md) — checklist and evidence record to complete during BIT-466.

Repository-document lifecycle policy and shared vocabulary remain canonical in the
[handbook](../../../docs/handbook/REF-001.md) and [glossary](../../../docs/glossary.md); the SPEC
defines the runtime aggregate's complete lifecycle.
