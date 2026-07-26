---
id: EPKG-<NNNN>
title: <Bounded delivery title>
status: draft
version: 0.1.0
owners: <Accountable owner>
last_updated: <YYYY-MM-DD>
prd: PRD-<NNN>
---

# EPKG-<NNNN>: <Bounded delivery title>

Create `README.md`, `SPEC.md`, `PROMPT.md`, `REVIEW.md`, and `TESTS.md` in the package directory.
Each file carries the package ID, version, owner, date, status, and a type suffix where applicable.

## Required content

- **README:** traceability and ordered navigation.
- **SPEC:** objective, governing PRD/ADRs, deliverables, constraints, and acceptance criteria.
- **PROMPT:** provider-neutral role, reading order, boundaries, and required outputs.
- **TESTS:** verification strategy, exact commands, expected evidence, and manual inspection.
- **REVIEW:** requirement mapping, actual results, findings, residual risks, and deferred decisions.

Use the [completed EPKG-0001](../.specs/epkg/EPKG-0001/README.md) as a concrete example; do not copy
its foundation-specific requirements.
