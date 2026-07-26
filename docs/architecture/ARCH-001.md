---
id: ARCH-001
title: Rocky System Architecture
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
---

# ARCH-001: Rocky System Architecture

## Purpose, authority, and scope

This technology-neutral baseline describes Rocky as the repository-native engineering framework
chartered by [RKY-000](../charters/RKY-000.md). Accepted [ADRs](../adr/README.md) remain authoritative
for decisions; this document connects them into a system view and must not override them. The
[glossary](../glossary.md) owns terminology.

The current system is a documentation framework, a metadata-only Python bootstrap, local quality
commands, and CI. The domain model below is an analysis model. In particular, **Artifact is an
architectural hypothesis, not an implemented class, service, persistence model, or API**.

## Capability status baseline

| Capability | Status | Evidence or boundary |
| --- | --- | --- |
| Repository-native knowledge artifacts and navigation | Implemented | Markdown artifacts, root and [documentation](../README.md) indexes. |
| Artifact templates and delivery checklists | Implemented | The [template index](../../templates/README.md). |
| Lint, static type, test, and local-link quality gates | Implemented | Root `Makefile`, tests, Python configuration, and CI workflow. |
| Formal architecture baseline and engineering asset catalog | Implemented as documentation | This baseline and [CAT-001](../catalog/CAT-001.md); no runtime model is implied. |
| Automated metadata, relationship, and schema validation | Partially implemented | Local links are checked; lifecycle metadata and semantic relationships require human review. |
| Runtime Artifact and Workspace management | Planned | Requires an accepted PRD, decisions, and a separate EPKG. No runtime code exists. |
| Persistence, graph traversal, external integrations, and AI providers | Conceptual | No technology, interface, vendor, or delivery commitment has been selected. |

“Implemented as documentation” means a maintained knowledge asset exists; it does not mean the
described future product capability is executable.

## System context

Maintainers, contributors, reviewers, and human-directed agents read and change repository
knowledge through ordinary version control. Local developer tools and CI evaluate the same quality
commands. Issue trackers may coordinate work, but are external references and never the canonical
source. No database, hosted service, external integration, autonomous agent, or AI provider is
inside the implemented system boundary.

```text
People and human-directed agents
              |
              v
  Rocky repository knowledge  ----> local quality tools / CI
              |
              v
       reviewed version history

External issue trackers and future providers: non-authoritative and outside the boundary
```

## Initial domain model

The model separates currently managed knowledge from hypotheses about a future runtime domain.

### Knowledge Asset model

A **Knowledge Asset** is the implemented documentation-level aggregate represented by files in the
repository. Its minimum conceptual attributes are:

| Element | Meaning | Current representation |
| --- | --- | --- |
| Identity | Stable series identifier and title | Front matter or indexed filename. |
| Classification | Asset kind, such as ADR, EPKG, ARCH, or CAT | Identifier prefix and catalog entry. |
| Lifecycle | Status, semantic version, and last-updated date | Front matter, governed by the handbook. |
| Accountability | Owner responsible for stewardship | `owners` metadata. |
| Content | Reviewable engineering intent, decision, guidance, or evidence | English Markdown. |
| Relationships | Governs, governed-by, supersedes, packages, or references links | Repository-relative Markdown links. |
| Evidence | Checks or review records supporting claims | TESTS and REVIEW assets where applicable. |

The repository and review process enforce this model socially and through link validation; there
is no runtime aggregate, schema registry, persistence mapping, or universal metadata parser.

### Conceptual relationships

```text
Product Charter -> Product Requirement -> Architecture Decision
                                      \-> Engineering Package -> Review evidence
Architecture Decision ----------------/
System Architecture -> describes constraints and bounded contexts
Engineering Asset Catalog -> inventories Knowledge Assets
Knowledge Asset -> relates to zero or more Knowledge Assets
Workspace (planned) -> could organize Artifacts (conceptual)
Artifact (conceptual) -> could represent structured engineering knowledge
```

Charters, PRDs, ADRs, EPKGs, architecture documents, catalogs, RFCs, patterns, lessons learned, and
postmortems are Knowledge Asset kinds. The proposed `Artifact` and `Workspace` names are placeholders
for future domain discovery, not a claim that all files already share a runtime abstraction.

## Bounded-context map

| Context | Responsibility | Current state | Relationship |
| --- | --- | --- | --- |
| Product Intent | Mission, outcomes, and testable requirements | Implemented as repository knowledge | Governs Architecture and Delivery Evidence. |
| Architecture Governance | System constraints, decisions, patterns, and proposals | Implemented as repository knowledge | Conforms to Product Intent; constrains Delivery Evidence. |
| Delivery Evidence | Bounded specifications, execution guidance, test plans, and reviews | Implemented as repository knowledge | Consumes Product Intent and Architecture Governance by reference. |
| Knowledge Catalog | Discovery, classification, ownership, lifecycle, and relationships | Implemented as documentation; automation partial | References all contexts without owning their canonical content. |
| Workspace Management | Organization and manipulation of runtime workspaces and artifacts | Planned | Must depend on published knowledge contracts if later approved. |
| Integration and Automation | External systems, persistence adapters, and AI-provider adapters | Conceptual | Must remain outside core policy and depend inward through explicit ports. |

The first four boundaries are semantic documentation contexts, not deployed services. No context
requires a process, network boundary, database, or independent release.

## Logical layers and dependency rule

From inward to outward, the logical layers are:

1. **Policy and domain knowledge:** chartered concepts, requirements, and accepted decisions;
   technology-independent and canonical.
2. **Use-case guidance:** EPKG specifications, prompts, test plans, reviews, templates, and
   checklists that apply policy to bounded work.
3. **Repository interfaces:** Markdown navigation, package metadata, and future explicit ports that
   expose knowledge without selecting infrastructure.
4. **Tooling and infrastructure:** current Make targets, Python development tools, link checker,
   Git, and CI; future storage, integration, and provider adapters would also belong here.

**Dependency rule:** knowledge and use-case layers must not depend on infrastructure, vendors,
storage engines, hosted services, or AI providers. Dependencies point inward toward stable policy;
outer layers may implement explicit inner contracts. Cross-context relationships use stable IDs and
repository-relative links rather than copied content. Cycles between normative authorities are not
allowed; the precedence rules in the [handbook](../handbook/REF-001.md) resolve governance order.

## Constraints and evolution

- New runtime domains require governing product requirements and a separate EPKG.
- A database, graph technology, serialization schema, service topology, or provider must be decided
  only when concrete requirements justify it; this baseline selects none.
- Accepted ADRs are changed only through their documented successor process.
- Capability status must be updated when evidence changes, and catalog entries must link to the
  canonical asset rather than restating it.
- Security-sensitive or private material stays outside repository context and is referenced only
  through an approved secure system.

## Deferred decisions

Runtime semantics for Artifact and Workspace; identifiers beyond repository knowledge assets;
storage and query needs; graph behavior; API and event contracts; process and deployment topology;
authorization and tenancy; integration boundaries; AI-provider ports; automated schema validation;
and migration/version compatibility are intentionally deferred.
