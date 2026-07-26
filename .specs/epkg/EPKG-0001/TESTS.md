---
id: EPKG-0001-TESTS
title: Rocky Engineering Framework foundation test plan
status: accepted
version: 1.0.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0001
---

# EPKG-0001 test plan

Run from the repository root in Python 3.11 or later after installing `.[dev]`.

| Gate | Command | Demonstrates |
| --- | --- | --- |
| Lint | `make lint` | Python source and checks satisfy configured style and correctness rules. |
| Type-check | `make type-check` | Strict static typing succeeds for source and tests. |
| Test | `make test` | Bootstrap package behavior passes. |
| Links | `make links` | Every repository-local Markdown target exists. |

Also inspect `git diff --check`, `git status --short`, and the complete diff. Review artifact IDs,
versions, dates, and links; search for unfinished markers (`TODO`, `TBD`, `FIXME`, `placeholder`);
and verify every acceptance criterion in the [SPEC](SPEC.md). Exact execution evidence belongs in
[REVIEW](REVIEW.md), not in this reusable plan.
