---
id: EPKG-0005-TESTS
title: Engagement Application Layer test plan
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0005
---

# EPKG-0005 test plan

## Test strategy

Tests exercise the application boundary with deterministic clocks and local repository fakes. They verify orchestration, persistence calls, DTO detachment, and error behavior while retaining EPKG-0004 domain tests as the authority for aggregate invariants.

No network, filesystem, database, framework, provider, or wall-clock dependency is permitted.

## Test double requirements

The test repository fake must:

- implement `get`, `add`, and `save`;
- record call order and counts;
- retain aggregates by canonical identity;
- support preloading an aggregate;
- reject duplicate `add` operations in a manner compatible with the application contract;
- remain test-only.

A fixed clock returns one timezone-aware timestamp and records invocation count.

## Creation scenarios

- creates a draft engagement from valid primitive inputs;
- constructs normalized domain values through the domain constructors;
- checks for an existing identity before creation;
- obtains exactly one timestamp;
- calls repository `add` exactly once;
- does not call `save`;
- returns an immutable complete view;
- raises `EngagementAlreadyExists` for an existing identity;
- performs no write when duplicate;
- propagates invalid identifier, actor, goal, or timestamp failures unchanged.

## Retrieval scenarios

- returns a complete immutable view for an existing engagement;
- raises `EngagementNotFound` for a missing identity;
- performs no `add` or `save`;
- does not invoke the clock;
- changing returned collections cannot mutate the aggregate;
- later aggregate mutation does not retroactively alter a previously returned view.

## Ownership and participant scenarios

For assign owner, add participant, and remove participant:

- loads the correct aggregate;
- obtains exactly one timestamp;
- invokes the matching public aggregate method;
- saves exactly once after success;
- returns updated state;
- raises `EngagementNotFound` without a write when absent;
- preserves typed domain errors such as owner-participant conflict, duplicate participant, missing participant, and terminal-state protection;
- performs no save after domain failure.

## Decision and milestone scenarios

For record decision, register milestone, and complete milestone:

- constructs required domain values;
- passes the command timestamp to the domain operation through the injected clock where applicable;
- saves exactly once after success;
- returns detached tuple-based history and milestone views;
- propagates invalid decision, invalid milestone, duplicate milestone, missing milestone, repeated completion, and terminal-state failures;
- performs no save after failure.

## Lifecycle scenarios

For start, suspend, resume, complete, and cancel:

- invokes only the corresponding aggregate method;
- uses one timezone-aware clock value;
- saves once after success;
- returns the new lifecycle state and timestamp;
- propagates invalid lifecycle transitions unchanged;
- does not save when the transition fails.

## Contract and architecture scenarios

- commands and queries are immutable;
- result DTOs and nested DTOs are immutable;
- result collections are tuples;
- handlers depend only on domain, application ports, and standard library;
- domain modules do not import application modules;
- repository protocol contains only `get`, `add`, and `save`;
- application public exports contain only approved contracts;
- no production in-memory adapter exists;
- no framework, ORM, HTTP, CLI, messaging, provider, or generic bus dependency is introduced.

## Quality gates

The implementation is reviewable only when all commands pass:

```shell
make lint
make type-check
make test
make links
make check
```

CI output and the final commit SHA must be recorded in [REVIEW.md](REVIEW.md). A checklist without command evidence is insufficient.
