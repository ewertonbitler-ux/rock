---
id: ARCH-001
title: Rocky System Architecture
status: proposed
version: 0.2.0
owners: Rocky maintainers
last_updated: 2026-07-26
---

# ARCH-001: Rocky System Architecture

## Purpose, authority, and scope

This technology-neutral baseline describes Rocky as the repository-native engineering framework
chartered by [RKY-000](../charters/RKY-000.md). Accepted [ADRs](../adr/README.md) remain authoritative
for decisions; this document connects them into a system view and must not override them. The
[glossary](../glossary.md) owns terminology.

The current system is a documentation framework, a Python Knowledge Asset core domain, local
quality commands, and CI. The repository documentation model below remains distinct from the
runtime aggregate. In particular, **Artifact is an
architectural hypothesis, not an implemented class, service, persistence model, or API**.

## Capability status baseline

| Capability | Status | Evidence or boundary |
| --- | --- | --- |
| Repository-native knowledge artifacts and navigation | Implemented | Markdown artifacts, root and [documentation](../README.md) indexes. |
| Artifact templates and delivery checklists | Implemented | The [template index](../../templates/README.md). |
| Lint, static type, test, and local-link quality gates | Implemented | Root `Makefile`, tests, Python configuration, and CI workflow. |
| Formal architecture baseline and engineering asset catalog | Implemented as documentation | This baseline and [CAT-001](../catalog/CAT-001.md); no runtime model is implied. |
| Knowledge Asset core domain and bounded application operations | Implemented | Persistence-free [`rocky.knowledge_assets`](../../src/rocky/knowledge_assets/) package and focused tests. |
| Automated metadata, relationship, and schema validation | Partially implemented | Local links are checked; lifecycle metadata and semantic relationships require human review. |
| Engagement Context | Proposed for specification | [PRD-002](../prd/PRD-002.md) and proposed [ADR-004](../adr/ADR-004.md); no Engagement code exists. |
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

The repository and review process enforce this documentation model socially and through link
validation. Separately, `rocky.knowledge_assets` implements the neutral identity, kind, status,
version, owner, logical content-reference, relationship, lifecycle, and bounded use-case rules
specified by EPKG-0003. It does not parse these files or provide a schema registry, persistence
mapping, or universal metadata parser.

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
| Engagement | Governed engineering engagements, ownership, participation, and traceability | Proposed for specification | Must conform to repository authority and publish bounded contracts without infrastructure dependencies. |
| Workspace Management | Organization and manipulation of runtime workspaces and artifacts | Planned | Must depend on published knowledge contracts if later approved. |
| Integration and Automation | External systems, persistence adapters, and AI-provider adapters | Conceptual | Must remain outside core policy and depend inward through explicit ports. |

The first four boundaries are semantic documentation contexts, not deployed services. No context
requires a process, network boundary, database, or independent release.

## Domain evolution

Knowledge remains a foundational concern, and Knowledge Asset remains an independent domain.
Engineering Domains evolve through their own boundaries. A new Engineering Domain requires an
accepted PRD and a dedicated EPKG; an ADR is required only for consequential, cross-cutting, or
difficult-to-reverse decisions. Proposed artifacts do not authorize implementation. Infrastructure
and provider concerns remain outside domain policy.

## Logical layers and dependency rule

From inward to outward, the logical layers are:

1. **Policy and domain knowledge:** chartered concepts, requirements, accepted decisions, and the
   persistence-free Knowledge Asset domain; technology-independent and canonical.
2. **Use-case guidance:** EPKG specifications, prompts, test plans, reviews, templates, checklists,
   and the bounded Knowledge Asset application operations that apply policy to work.
3. **Repository interfaces:** Markdown navigation, package metadata, and the abstract Knowledge
   Asset repository port, which exposes required storage capabilities without selecting infrastructure.
4. **Tooling and infrastructure:** current Make targets, Python development tools, link checker,
   Git, and CI; future storage, integration, and provider adapters would also belong here.

**Dependency rule:** knowledge and use-case layers must not depend on infrastructure, vendors,
storage engines, hosted services, or AI providers. Dependencies point inward toward stable policy;
outer layers may implement explicit inner contracts. Cross-context relationships use stable IDs and
repository-relative links rather than copied content. Cycles between normative authorities are not
allowed; the precedence rules in the [handbook](../handbook/REF-001.md) resolve governance order.

## Constraints and evolution

- New Engineering Domains require an accepted PRD and a separate EPKG; a further ADR is required only for consequential or cross-cutting architecture decisions. Engagement remains proposed for specification under [PRD-002](../prd/PRD-002.md) and proposed [ADR-004](../adr/ADR-004.md).
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
