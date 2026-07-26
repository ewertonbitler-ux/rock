---
id: EPKG-0005-PROMPT
title: Engagement Application Layer implementation prompt
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0005
---

# EPKG-0005 implementation prompt

## Role

Act as a senior Python engineer implementing the application boundary specified by [EPKG-0005](SPEC.md). Preserve the Engagement aggregate delivered by [EPKG-0004](../EPKG-0004/SPEC.md) as the sole owner of business invariants.

## Required implementation

Create `rocky.engagements.application` with:

- immutable command DTOs for every approved aggregate mutation;
- immutable `GetEngagement` query;
- explicit handlers;
- immutable detached result DTOs;
- `EngagementRepository` protocol;
- `Clock` callable contract;
- `EngagementApplicationError`, `EngagementNotFound`, and `EngagementAlreadyExists`;
- focused tests described in [TESTS.md](TESTS.md).

## Implementation rules

1. Do not modify domain invariants merely to simplify handlers.
2. Use only public Engagement behavior.
3. Mutating handlers load or create one aggregate, obtain one clock value, invoke one domain operation, and persist once after success.
4. Do not save after any validation or domain failure.
5. Let typed domain exceptions propagate unchanged.
6. Return immutable DTOs detached from aggregate-owned mutable state.
7. Keep repository behavior limited to `get`, `add`, and `save`.
8. Define test fakes inside tests; do not add a production in-memory adapter.
9. Do not introduce a command bus, mediator, generic handler registry, unit of work, DI framework, service locator, ORM, API framework, serialization layer, or provider integration.
10. Preserve strict typing and the repository's formatting conventions.

## Suggested implementation sequence

1. Add application errors and ports.
2. Add result DTOs and private mapping logic.
3. Add commands and query.
4. Implement creation and retrieval handlers.
5. Implement ownership and participant handlers.
6. Implement decision and milestone handlers.
7. Implement lifecycle handlers.
8. Export the justified public API.
9. Add focused tests and run `make check`.
10. Update REVIEW.md with actual evidence only after commands pass.

## Completion constraints

Do not claim completion based only on code presence. Completion requires:

- all acceptance criteria in SPEC.md demonstrated;
- all scenarios in TESTS.md covered;
- `make check` passing;
- architecture and public API review completed;
- REVIEW.md updated with real commit and CI evidence.
