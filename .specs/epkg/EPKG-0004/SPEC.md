---
id: EPKG-0004-SPEC
title: Engagement Core Domain specification
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0004
---

# EPKG-0004 specification

## Objective and authority

EPKG-0004 implements the accepted requirements in
[PRD-002](../../../docs/prd/PRD-002.md). The package defines one technology-neutral Engagement
boundary and must remain consistent with the accepted ADRs and
[ARCH-001](../../../docs/architecture/ARCH-001.md).

Repository documents remain the source of product and architecture authority. The runtime domain
does not parse, replace, or own those documents.

## Aggregate boundary

`Engagement` is the aggregate root and consistency boundary for one governed engineering
engagement. All mutation occurs through aggregate behavior.

The aggregate owns:

- immutable `EngagementId`;
- exactly one accountable owner;
- one engineering goal;
- participants;
- lifecycle state;
- immutable decision history;
- milestones and their completion state;
- creation and last-update timestamps.

The aggregate does not own external identity records, repositories, tickets, documents, files,
persistence, clocks, APIs, messaging, integrations, or AI orchestration.

## Value objects and entity

- `EngagementId`: canonical `ENG-` followed by exactly four ASCII digits; validated, immutable, and
  case-sensitive.
- `Actor`: normalized external actor reference containing identifier and display name. Equality uses
  the complete normalized value; actor lookup is out of scope.
- `Participant`: immutable actor and role pair.
- `Goal`: immutable title and description.
- `Decision`: immutable timezone-aware timestamp, author, rationale, and outcome.
- `Milestone`: engagement-owned entity with stable normalized identifier, name, status, and optional
  completion timestamp.

Text values normalize Unicode to NFC, collapse whitespace, reject empty/control-character content,
and enforce the implementation limits defined in the runtime code.

## Lifecycle

Statuses are `draft`, `active`, `suspended`, `completed`, and `cancelled`.

| From | Allowed transition |
| --- | --- |
| draft | start → active; cancel → cancelled |
| active | suspend → suspended; complete → completed; cancel → cancelled |
| suspended | resume → active; cancel → cancelled |
| completed | none |
| cancelled | none |

Same-state and all unlisted transitions are invalid. Completed and cancelled engagements are
terminal and reject further owner, participant, decision, milestone, or lifecycle mutation.

## Ownership and participation invariants

- An engagement always has exactly one owner.
- The owner cannot simultaneously be a participant.
- Participant uniqueness is case-insensitive by normalized actor identifier.
- Assigning an existing participant as owner fails.
- Adding the current owner as participant fails.
- Removing a missing participant fails.

## Decision invariants

- Decisions are immutable values.
- Recorded decisions are append-only and exposed through a read-only tuple.
- Corrections require a new decision; existing decisions are never edited or removed.
- Decision timestamps must be timezone-aware.

## Milestone invariants

- Milestone identifiers are unique case-insensitively within one engagement.
- Milestones begin as `planned`.
- Completion requires a timezone-aware timestamp.
- A completed milestone cannot be completed again or reverted.
- A missing milestone cannot be completed.
- Milestones are exposed through a read-only tuple; collection replacement is not public behavior.

## Public behavior

The justified public aggregate operations are:

- `create`;
- `assign_owner`;
- `add_participant` and `remove_participant`;
- `record_decision`;
- `register_milestone` and `complete_milestone`;
- `start`, `suspend`, `resume`, `complete`, and `cancel`.

These are domain capabilities, not generic CRUD. No repository port or application service is
required by this package because PRD-002 authorizes only the domain representation and behavior.

## Domain errors

Expose `EngagementError` and specific failures for invalid identifiers, actors, goals, decisions,
milestones, lifecycle transitions, duplicate/missing participants and milestones, owner-participant
conflicts, and repeated milestone completion. Public behavior must not document generic
`ValueError`, `KeyError`, or assertions as domain outcomes.

## Module structure and dependency rule

```text
src/rocky/
  engagements/
    __init__.py
    domain.py
    errors.py
tests/
  engagements/
    test_engagement.py
```

The domain imports only the Python standard library and its own errors. It must not import other
Rocky domains, application layers, infrastructure, frameworks, providers, files, Markdown, Git, or
external services.

## Acceptance criteria

1. One `Engagement` aggregate implements all lifecycle transitions and terminal-state protection.
2. Owner and participant invariants are observable through typed domain failures.
3. Decision history is immutable and append-only.
4. Milestone uniqueness and completion invariants are enforced.
5. Public collections cannot mutate aggregate-owned collections directly.
6. Domain code is persistence-free and provider-neutral.
7. Ruff, strict mypy, pytest, architecture checks, and Markdown link checks pass through `make check`.

## Explicit exclusions

EPKG-0004 excludes persistence, repository ports, APIs, CLI, UI, authentication, authorization,
domain events, event buses, messaging, external identity lookup, Jira/GitHub/Confluence/Slack/SAP
integration, AI orchestration, document parsing, and additional Engineering Domains.