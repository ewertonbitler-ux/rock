---
id: EPKG-0003-TESTS
title: Knowledge Asset Core Domain test plan
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0003
issue: BIT-466
preparation_issue: BIT-470
---

# EPKG-0003 test plan

BIT-466 must add focused tests that demonstrate behavior at public boundaries rather than internal
implementation. At minimum verify:

- validation, normalization, immutability, hashing, and equality for every value object, including
  valid/invalid ID and kind-prefix pairs, open kind extensions, content references, and typed errors;
- aggregate construction, read-only state, required owners, and invalid construction;
- every valid and invalid cell in the complete lifecycle matrix, same-state requests, terminal and
  non-terminal behavior, and a stricter series policy that cannot relax generic rules;
- accepted-asset evolution, increasing draft/proposed versions, immutable accepted versions,
  explicit distinct successors, and superseded history;
- owner normalization, case-folded duplicates, adding/removing owners, and last-owner protection;
- canonical SemVer validation, precedence, build-metadata equality, and forbidden regression;
- relationship direction and inverse mapping, duplicate prevention, self-reference, exact removal,
  multiple relationship types to one target, explicitly stored versus derived reciprocal behavior,
  and missing targets;
- every included application use case with test-local repository doubles, including source not
  found, target not found, duplicate create, save/no-save behavior on success/failure, and propagated
  repository failures;
- architecture/import boundaries: domain independence, inward application/port dependencies, and
  absence of production adapters, forbidden frameworks, runtime `Artifact`, and excluded modules.

Run these commands from the repository root after installing the development dependencies:

| Gate | Command | Required evidence |
| --- | --- | --- |
| Lint | `make lint` | Exit code and exact summary. |
| Type-check | `make type-check` | Exit code and checked-file summary. |
| Tests | `make test` | Exit code and test count/summary. |
| Links | `make links` | Exit code and link-check summary. |
| Aggregate regression | `make check` | Exit code and all component summaries. |
| Whitespace | `git diff --check` | Exit code and any output. |

Then inspect `git status --short`, the complete diff (including untracked files), and every changed
Markdown link. Reconcile lifecycle language across SPEC, tests, ARCH-001, CAT-001, REF-001, and the
glossary; check for duplicated canonical policy, secrets, unfinished markers, unrelated changes,
runtime `Artifact`, and prohibited infrastructure. Record exact observed results, changed files,
decisions, unresolved questions, and the runtime-domain scope confirmation in
[REVIEW](REVIEW.md).
