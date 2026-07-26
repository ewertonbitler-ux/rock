---
id: EPKG-0003-REVIEW
title: Knowledge Asset Core Domain implementation review
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0003
issue: BIT-466
preparation_issue: BIT-470
---

# EPKG-0003 implementation review

This record contains the completed BIT-466 implementation evidence. Only a maintainer may accept
the package.

## Traceability and scope checklist

- [x] Implementation maps to every [SPEC](SPEC.md) acceptance criterion.
- [x] `KnowledgeAsset` is the sole new runtime aggregate and protects its boundary and invariants.
- [x] Value objects implement the specified validation, normalization, equality, and immutability.
- [x] The full lifecycle matrix, accepted evolution, successor behavior, and policy extension agree
      with the SPEC.
- [x] Ownership, content reference, and relationships follow the specified neutral semantics.
- [x] Public failures use explicit domain/application errors rather than generic exception leakage.
- [x] Only the enumerated intention-revealing use cases and minimal repository port were added.
- [x] No runtime `Artifact`, excluded domain, generic CRUD, speculative layer, adapter, framework,
      parser, provider, persistence, integration, or inaccessible authority was introduced.
- [x] ARCH-001 and CAT-001 contain factual runtime status and no premature acceptance claim.

## Test coverage checklist

- [x] Value-object validation and equality tests.
- [x] Aggregate-construction and immutable-state tests.
- [x] Full valid lifecycle transition matrix and invalid-transition tests.
- [x] Accepted-asset evolution, version, successor, and supersession tests.
- [x] Ownership normalization, duplication, and last-owner tests.
- [x] Relationship direction, duplication, self-reference, reciprocal-policy, removal, and target tests.
- [x] All application use cases tested with test-local repository doubles.
- [x] Architecture/import-boundary and forbidden-scope tests.
- [x] All existing repository tests and gates remain passing.

## Validation evidence

Record exact output and exit code after execution; do not prefill results.

| Command | Exit code | Exact result |
| --- | --- | --- |
| `make lint` | 0 | `All checks passed!` |
| `make type-check` | 0 | `Success: no issues found in 12 source files` |
| `make test` | 0 | `88 passed in 0.15s` |
| `make links` | 0 | `All relative Markdown links resolve.` |
| `make check` | 0 | Ruff passed; mypy checked 12 source files; `88 passed in 0.14s`; all relative Markdown links resolve. |
| `git diff --check` | 0 | No output. |

## Manual inspection

- [x] Complete tracked and untracked diff inspected.
- [x] Every changed Markdown link inspected and link validation reconciled.
- [x] Lifecycle consistency reviewed across code, tests, SPEC, ARCH-001, CAT-001, REF-001, and glossary.
- [x] Duplication against ARCH-001, CAT-001, REF-001, and glossary reviewed.
- [x] Changed-file list contains no unrelated work, secret, stale metadata, or unfinished marker.
- [x] Commit references BIT-466 and EPKG-0003; pull request targets `main` and reports exact evidence.

## Completion record

### Files created or changed

- `src/rocky/knowledge_assets/{domain,errors}.py`: aggregate, value objects, policy protocol, and
  explicit failures.
- `src/rocky/knowledge_assets/{application,ports}.py`: enumerated use cases and minimal repository
  protocol; `__init__.py` exposes the public domain surface.
- `tests/knowledge_assets/`: public-boundary value, aggregate, lifecycle, and application tests.
- `tests/test_architecture.py`: inward-import and excluded-scope regression tests.
- `README.md`, `docs/architecture/ARCH-001.md`, and `docs/catalog/CAT-001.md`: factual runtime status
  and navigation, while retaining the distinction from repository documents.
- `.specs/epkg/EPKG-0003/REVIEW.md`: this execution evidence.

### Decisions realized

- Immutable dataclass value objects provide concrete-type value equality; aggregate collections
  are returned as `frozenset` snapshots, the transition matrix is deeply immutable, and mutations
  occur only through domain methods. The aggregate constructor validates its domain-value inputs
  and creates only a draft.
- The closed status and relationship types use `StrEnum`; kinds remain open through an explicit
  factory with no process-global extension registry, and relationship inverses use an explicit map.
- SemVer precedence is implemented locally without a dependency; build metadata remains part of
  equality while being excluded from precedence.
- Application functions express only the approved intentions and use a test-local repository fake.

### Findings, unresolved questions, and deferrals

None observed. Persistence, concurrent deletion, inverse traversal/repair, content storage,
serialization, events, audit history, and every other SPEC deferral remain future decision paths
owned by Rocky maintainers.

### Runtime-domain confirmation

The approved Knowledge Asset runtime aggregate, values, errors, policy boundary, minimal repository
port, and enumerated operations are implemented. Runtime Artifact, Workspace, other excluded
domains, persistence adapters, generic CRUD, frameworks, external integrations, Markdown parsing,
filesystem behavior, web APIs, UI, authentication, tenancy, and AI orchestration remain
unimplemented.

### Approval

Pending maintainer review through normal repository controls. No architectural or package
acceptance is claimed by this implementation record.
