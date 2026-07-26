---
id: EPKG-0005-SPEC
title: Engagement Application Layer specification
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0005
---

# EPKG-0005 specification

## Objective and authority

EPKG-0005 exposes the Engagement behavior delivered by [EPKG-0004](../EPKG-0004/SPEC.md) through a small, provider-neutral application boundary. It remains governed by [PRD-002](../../../docs/prd/PRD-002.md), accepted ADRs, and [ARCH-001](../../../docs/architecture/ARCH-001.md).

Repository knowledge remains authoritative. The application layer coordinates runtime behavior but does not parse, replace, or own product, architecture, package, or review documents.

## Architectural decisions

1. The application layer coordinates use cases; it does not contain Engagement invariants.
2. Commands request state changes. Queries request read-only results.
3. Every mutating handler loads or creates one Engagement aggregate, invokes public domain behavior, and saves only after successful execution.
4. A minimal `EngagementRepository` protocol is owned by the application boundary.
5. No concrete persistence adapter is delivered. Tests use local fakes defined in the test suite.
6. Time is supplied through an injected `Clock` callable so application tests remain deterministic.
7. Public handlers return immutable DTOs rather than exposing mutable aggregate internals.
8. Domain failures remain domain failures. The application layer adds only failures that arise from orchestration, such as an engagement not being found.
9. A generic command bus, mediator, unit-of-work framework, dependency-injection container, or service locator is not justified in this package.
10. Concurrency control is deferred until a concrete persistence requirement exists.

## Application boundary

```text
Caller
  |
  v
Command or Query Handler
  |              |
  |              +--> Clock
  |
  +--> EngagementRepository
  |
  v
Engagement aggregate
```

Dependencies point inward. `rocky.engagements.application` may import `rocky.engagements.domain` and `rocky.engagements.errors`. Domain code must not import application code.

## Repository port

The application layer requires the following behavior:

```python
class EngagementRepository(Protocol):
    def get(self, engagement_id: EngagementId) -> Engagement | None: ...
    def add(self, engagement: Engagement) -> None: ...
    def save(self, engagement: Engagement) -> None: ...
```

Semantics:

- `get` returns the aggregate or `None` when absent;
- `add` persists a newly created aggregate and must reject an existing identity;
- `save` persists changes to an existing aggregate;
- transaction boundaries, storage technology, serialization, versioning, and locking are outside this package.

The protocol must not expose generic list, delete, filter, query-language, session, transaction, or ORM behavior.

## Clock port

```python
Clock = Callable[[], datetime]
```

The returned timestamp must be timezone-aware. Handlers obtain one timestamp per command and pass that value to domain behavior. Queries do not require a clock.

## Commands

Immutable command DTOs are required for:

- `CreateEngagement`;
- `AssignOwner`;
- `AddParticipant`;
- `RemoveParticipant`;
- `RecordDecision`;
- `RegisterMilestone`;
- `CompleteMilestone`;
- `StartEngagement`;
- `SuspendEngagement`;
- `ResumeEngagement`;
- `CompleteEngagement`;
- `CancelEngagement`.

Commands contain primitive input values or immutable domain identifiers. They must not contain repositories, handlers, mutable aggregates, infrastructure sessions, request objects, or provider-specific values.

## Queries

The first application boundary requires:

- `GetEngagement` by canonical `EngagementId`.

List, search, pagination, reporting, filtering, graph traversal, and cross-context queries are deferred because PRD-002 does not define those needs.

## Handlers

Each use case is implemented by an explicit handler class or function with one public `handle` operation.

### Create Engagement

1. Construct `EngagementId`, `Actor`, and `Goal` from command input.
2. Fail with `EngagementAlreadyExists` when the repository already contains the identity.
3. Obtain one timestamp from the clock.
4. Call `Engagement.create`.
5. Add the aggregate to the repository.
6. Return an immutable `EngagementView`.

### Mutating an existing Engagement

1. Construct and validate the canonical identity.
2. Load the aggregate.
3. Fail with `EngagementNotFound` when absent.
4. Obtain one timestamp from the clock.
5. Invoke exactly one public aggregate behavior, constructing required value objects.
6. Save only after the domain operation succeeds.
7. Return the updated immutable view.

A handler must not catch and replace typed domain failures with generic application errors.

### Get Engagement

1. Construct and validate the canonical identity.
2. Load the aggregate.
3. Fail with `EngagementNotFound` when absent.
4. Return the immutable view without saving.

## Result DTOs

`EngagementView` is an immutable application result containing:

- engagement identifier;
- owner view;
- goal view;
- lifecycle status;
- creation and update timestamps;
- participant views;
- decision views;
- milestone views.

Nested DTOs are immutable and detached from mutable aggregate-owned entities. Collections are tuples. The DTO is an application contract, not a JSON schema or persistence model.

## Application errors

Expose an `EngagementApplicationError` base and these specific failures:

- `EngagementNotFound`;
- `EngagementAlreadyExists`.

Repository implementation failures, network failures, database exceptions, transport errors, authorization failures, and retry policy are not modeled until a concrete adapter or requirement exists.

## Proposed module structure

```text
src/rocky/engagements/
  __init__.py
  domain.py
  errors.py
  application/
    __init__.py
    commands.py
    queries.py
    handlers.py
    dto.py
    errors.py
    ports.py
tests/
  engagements/
    test_engagement.py
    application/
      test_create_engagement.py
      test_get_engagement.py
      test_ownership_and_participants.py
      test_decisions_and_milestones.py
      test_lifecycle.py
      test_application_contracts.py
```

A separate top-level `ports` package is not introduced because the repository and clock contracts are required only by this application boundary. They remain colocated with the application layer that owns them.

## Public API

`rocky.engagements.application` exports only:

- command and query DTOs;
- handlers;
- result DTOs;
- application errors;
- `EngagementRepository` and `Clock` contracts.

Implementation helpers and DTO mapping functions remain private.

## Acceptance criteria

1. Every approved Engagement mutation is reachable through one explicit application command.
2. `GetEngagement` returns a detached immutable view.
3. Handlers contain orchestration only and delegate all business validity to the aggregate.
4. Mutating handlers save exactly once after successful domain behavior and never save after failure.
5. Creation rejects duplicate identities before adding a new aggregate.
6. Missing aggregates raise `EngagementNotFound`.
7. Domain failures pass through unchanged.
8. One timezone-aware clock value is used consistently for each mutation.
9. The repository protocol remains minimal and infrastructure-neutral.
10. No concrete persistence, transport, framework, provider, generic bus, or unit-of-work abstraction is added.
11. Ruff, strict mypy, pytest, architecture checks, and Markdown link checks pass through `make check`.

## Explicit exclusions

EPKG-0005 excludes concrete in-memory or database adapters in production code, ORM mappings, serialization, REST or GraphQL APIs, CLI, UI, authentication, authorization, tenant policy, concurrency tokens, transactions, retries, idempotency keys, event publication, generic CQRS infrastructure, command buses, service locators, Workspace, Knowledge Asset orchestration, external integrations, and AI orchestration.
