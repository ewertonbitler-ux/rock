---
id: EPKG-0005
title: Engagement Application Layer
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
prd: PRD-002
predecessor: EPKG-0004
---

# EPKG-0005: Engagement Application Layer

## Purpose

Define and implement the application boundary that coordinates the persistence-free Engagement aggregate delivered by [EPKG-0004](../EPKG-0004/README.md).

The package introduces explicit application commands, queries, handlers, result DTOs, application errors, and the minimum repository port required to execute Engagement use cases without selecting a database, framework, transport, provider, or deployment model.

## Authorized outcome

A caller can create, retrieve, and govern an Engagement through stable application contracts. Application handlers load an aggregate through an inward-facing repository port, invoke domain behavior, persist successful state changes, and return immutable results suitable for future adapters.

## Package artifacts

- [Specification](SPEC.md)
- [Implementation prompt](PROMPT.md)
- [Test plan](TESTS.md)
- [Review record](REVIEW.md)

## Architectural position

```text
External adapter (future)
          |
          v
Engagement application commands and queries
          |
          +----> EngagementRepository port
          |
          v
Engagement aggregate
```

The application layer depends on the Engagement domain. Infrastructure may later implement the repository port, but neither domain nor application code may depend on infrastructure.

## Scope summary

EPKG-0005 includes:

- command and query contracts;
- handlers for the approved Engagement use cases;
- immutable result DTOs;
- typed application failures;
- a minimal repository protocol;
- deterministic clock injection at the application boundary;
- focused unit tests using test doubles.

It excludes database adapters, ORM mappings, HTTP or CLI interfaces, serialization schemas, authentication, authorization, event buses, external integrations, Workspace, and generic application-framework abstractions.

## Delivery status

This package is proposed. Implementation is authorized only after its specification and test plan are reviewed against PRD-002, EPKG-0004, accepted ADRs, and ARCH-001.
