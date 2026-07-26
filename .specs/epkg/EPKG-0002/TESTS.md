---
id: EPKG-0002-TESTS
title: Rocky architecture baseline test plan
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0002
issue: BIT-465
---

# EPKG-0002 test plan

Run from the repository root with the existing development environment.

| Gate | Command | Demonstrates |
| --- | --- | --- |
| Lint | `make lint` | Existing Python style and correctness remain intact. |
| Type-check | `make type-check` | Existing strict typing remains intact. |
| Tests | `make test` | Existing bootstrap behavior remains intact. |
| Links | `make links` | Repository-local Markdown targets resolve. |
| Aggregate | `make check` | The repository's authoritative aggregate gate passes. |
| Whitespace | `git diff --check` | The patch has no whitespace errors. |

Manually inspect the full diff and every changed Markdown link. Verify capability-state language,
asset locations and metadata, canonical terminology, template-only placeholders, all acceptance
criteria, and the absence of runtime domain code or technology selection. Record exact evidence in
[REVIEW](REVIEW.md).
