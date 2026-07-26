---
id: EPKG-0003-SPEC
title: Knowledge Asset Core Domain specification
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0003
issue: BIT-466
preparation_issue: BIT-470
---

# EPKG-0003 specification

## Objective, authority, and scope

BIT-466 implements `KnowledgeAsset` as Rocky's first runtime aggregate and only the application
operations needed to exercise its approved behavior. This specification applies the architecture
baseline in [ARCH-001](../../../docs/architecture/ARCH-001.md) and the accepted decisions
[ADR-001](../../../docs/adr/ADR-001.md), [ADR-002](../../../docs/adr/ADR-002.md), and
[ADR-003](../../../docs/adr/ADR-003.md). Repository documents remain canonical knowledge under
ADR-002; the new runtime model does not parse or replace them.

`Artifact` remains an architectural hypothesis. BIT-466 must not implement it as a class, entity,
service, API, persistence model, alias, base class, or protocol. Nor may `KnowledgeAsset` be named
or exposed as `Artifact`.

## Aggregate boundary and invariants

`KnowledgeAsset` owns its stable ID, kind, status, semantic version, non-empty owner set, optional
logical content reference, and set of typed outbound relationships. It protects these invariants:

- every instance has a valid, immutable ID, kind, version, and at least one owner;
- its lifecycle changes only through the valid transition behavior below;
- accepted content cannot evolve structurally in place;
- relationship source is implicitly this aggregate; targets are other IDs, never loaded objects;
- no duplicate or self relationship can enter the owned relationship set;
- supersession has an explicit, distinct successor and consistent relationship semantics.

`AssetRelationship` is an immutable value object owned in the aggregate's relationship collection.
It consists of a relationship type and target `KnowledgeAssetId`; it does not own or load the
target. Target assets, repository storage, content bodies, identity directories, clocks, and
series-specific policy implementations remain outside the aggregate. The aggregate exposes state
read-only and changes it only through domain behavior; callers cannot mutate internal collections.

## Value objects

All value objects are immutable and compare by their normalized value and concrete semantic type.
They reject invalid construction with the explicit domain errors described below.

### KnowledgeAssetId

The stable representation is `<KIND>-<NUMBER>`, where `KIND` is 2–16 uppercase ASCII letters and
`NUMBER` is exactly 3 or 4 ASCII digits. The kind prefix belongs to the identifier and participates
in equality. IDs are case-sensitive and canonical: input is validated, not silently uppercased or
trimmed. Examples include `ADR-001`, `PRD-001`, `EPKG-0003`, `ARCH-001`, and `SPEC-0001`.

Invalid examples include `adr-001` (wrong case), `ADR-1` (wrong width), `ADR-00001` (wrong width),
`ADR_001` (separator), `ADR-ABC` (non-numeric), `A-001` (short prefix),
`LESSONLEARNEDASSET-001` (prefix longer than 16), and strings with surrounding whitespace. The
numeric portion may contain zeros, including an all-zero established series ID such as `RKY-000`; the core
does not allocate IDs or infer sequence. Kind and ID prefix must agree by the canonical prefix map
below, otherwise construction fails.

### KnowledgeAssetKind

Kind is an immutable, validated open value object rather than a closed language enum. The core
publishes canonical constants and prefix mappings for:

| Kind | Canonical prefix |
| --- | --- |
| Product Charter | `RKY` |
| PRD | `PRD` |
| ADR | `ADR` |
| EPKG | `EPKG` |
| SPEC | `SPEC` |
| PROMPT | `PROMPT` |
| REVIEW | `REVIEW` |
| TESTS | `TESTS` |
| ARCH | `ARCH` |
| CAT | `CAT` |
| RFC | `RFC` |
| Pattern | `PAT` |
| Lesson Learned | `LL` |
| Postmortem | `PM` |
| Checklist | `CHECK` |
| Template | `TMPL` |

Extension is allowed through a public factory accepting a canonical display name and a valid,
previously unclaimed prefix; this avoids a release for every new knowledge series. Equality uses
the exact canonical `(name, prefix)` pair and is case-sensitive. Empty, padded, control-character,
or conflicting name/prefix pairs fail. Extension registration, if used, is passed explicitly to
construction or policy and must not rely on a mutable process-global registry.

### KnowledgeAssetStatus and lifecycle

Status is a closed enum because transition exhaustiveness is a protected invariant: `draft`,
`proposed`, `accepted`, `rejected`, `superseded`, `deprecated`, and `archived`.

| From ↓ / To → | draft | proposed | accepted | rejected | superseded | deprecated | archived |
| --- | --- | --- | --- | --- | --- | --- | --- |
| draft | — | valid | invalid | invalid | invalid | invalid | valid |
| proposed | invalid | — | valid | valid | invalid | invalid | valid |
| accepted | invalid | invalid | — | invalid | valid* | valid | valid |
| rejected | invalid | invalid | invalid | — | invalid | invalid | valid |
| superseded | invalid | invalid | invalid | invalid | — | valid | valid |
| deprecated | invalid | invalid | invalid | invalid | invalid | — | valid |
| archived | invalid | invalid | invalid | invalid | invalid | invalid | — |

`*` Superseding requires an explicit successor summary with an ID distinct from the asset ID, the
same kind, `accepted` status, and a version greater in SemVer precedence. The summary is a domain
value supplied by the application after loading the successor, not a nested aggregate or repository
lookup. The aggregate records an outbound `superseded-by` relationship atomically with the
transition. A same-status request is an invalid transition, not an idempotent success. `archived`
is terminal. `rejected` and `superseded` are non-terminal only because they may be archived;
`superseded` may additionally be
deprecated to signal compatibility discouragement. All other states are non-terminal.

Deprecation says a formerly accepted or superseded asset remains discoverable for history or
compatibility but should not be selected for new work. Archival removes any applicable state from
ordinary active use while retaining history. Neither deletes content. Only accepted or superseded
assets can be deprecated. Any non-archived state can be archived.

Series-specific policy may reject a transition that the matrix permits, but cannot permit one the
matrix rejects or weaken aggregate invariants. It is an injected domain policy protocol expressed
only in domain values and transition intent; it has no Markdown, front-matter, file, Git, provider,
or repository dependency. With no supplied policy, the generic matrix applies.

### SemanticVersion

`SemanticVersion` accepts only canonical SemVer 2.0.0 strings: numeric `major.minor.patch` without
leading zeros, optionally followed by valid dot-separated prerelease identifiers and build
metadata. It rejects whitespace, a leading `v`, missing components, empty identifiers, leading
zeros in numeric prerelease identifiers, and non-ASCII identifier characters. Precedence and
equality follow SemVer: precedence ignores build metadata, while value-object equality compares the
entire canonical string, including build metadata.

Lifecycle transitions do not implicitly change version. Draft and proposed structural evolution
may explicitly replace the version through aggregate behavior and must provide a version greater
in SemVer precedence. Accepted assets may not mutate version or structural content in place; their
structural evolution requires a separately constructed asset with a greater version and either a
new stable ID or an explicitly modeled successor, then the original is superseded. Superseded,
deprecated, rejected, and archived assets cannot change version. Version rules contain no Git tag,
filename, or storage assumption.

### Owner

`Owner` is an accountable label, not an external identity. Construction trims leading/trailing
whitespace, collapses internal Unicode whitespace runs to one ASCII space, and Unicode-normalizes
to NFC. Empty values, control characters, or values longer than 200 Unicode code points fail.
Equality and hashing use the normalized value with Unicode case folding, while the normalized
display form is retained. An asset has a non-empty set of owners; adding an equivalent owner is a
duplicate error, and removing the last owner fails. No directory, authentication system, or
identity-provider lookup occurs.

### Relationships

The closed relationship-type enum defines these directed pairs:

| Outbound type | Derived inverse |
| --- | --- |
| `governs` | `governed-by` |
| `supersedes` | `superseded-by` |
| `packages` | `packaged-by` |
| `references` | `referenced-by` |
| `implements` | `implemented-by` |
| `validates` | `validated-by` |

Both names express direction and may be used as outbound relationship types. The aggregate stores
only the explicitly added outbound `(type, target ID)` value; inverse edges are derived by query or
application code and are never written automatically. Therefore adding `references B` does not
also store `referenced-by B` on the same source or mutate B. An identical type/target pair is a
duplicate; a different type to the same target is allowed. Every self-targeting relationship is
invalid. Removal requires an exact existing pair. Supersession behavior uses `superseded-by` on the
old asset; the reciprocal `supersedes` edge on the successor is not automatic.

Relationship construction does not establish target existence. Application use cases that have a
repository available must check existence before saving a newly added relationship or performing
supersession and return `RelationshipTargetNotFound`; the aggregate itself stays persistence-free.
Concurrent deletion and cross-aggregate reciprocal consistency are deferred to future persistence
requirements rather than hidden in this package.

### Logical content reference

`ContentReference` is an optional immutable opaque logical key with a required scheme and value,
serialized as `<scheme>:<value>`. Scheme is lowercase ASCII letters followed by lowercase letters,
digits, `+`, `.`, or `-`; value is non-empty, unpadded, contains no whitespace/control characters,
and is at most 500 code points. Equality is exact and case-sensitive after validation. The core
defines no schemes and does not interpret values. Filesystem paths, URLs, Markdown, Git references,
and provider-specific identifiers are neither special-cased nor parsed; adapters may map a neutral
logical reference outside the domain.

## Domain errors

Expose a `KnowledgeAssetError` base and specific public failures:

- `InvalidKnowledgeAssetId`, `InvalidKnowledgeAssetKind`, `KindIdentifierMismatch`;
- `InvalidSemanticVersion`, `VersionRegression`, `ImmutableAcceptedAsset`;
- `InvalidOwner`, `DuplicateOwner`, `LastOwnerRemoval`;
- `InvalidContentReference`;
- `InvalidLifecycleTransition`, `SuccessorRequired`, `InvalidSuccessor`;
- `InvalidRelationship`, `DuplicateRelationship`, `RelationshipNotFound`,
  `RelationshipTargetNotFound`;
- `SeriesPolicyViolation`.

Public constructors and behavior must not leak a generic `ValueError`, `KeyError`, or assertion as
their documented domain contract. Standard-library parsing failures are translated at the domain
boundary while preserving a useful message and structured offending value where safe.

## BIT-466 application use cases

BIT-466 includes exactly these application commands/queries:

1. create and save a draft asset from validated values;
2. propose a draft asset;
3. accept or reject a proposed asset;
4. deprecate an accepted or superseded asset;
5. archive any non-archived asset allowed by policy;
6. supersede an accepted asset with an explicit, existing, accepted successor of the same kind and
   a greater semantic version;
7. add or remove one typed outbound relationship, validating target existence when adding;
8. retrieve an asset by ID as the common prerequisite for commands.

These are intention-revealing operations, not generic CRUD. Creation fails rather than overwrites
an existing ID. Mutating operations load, invoke aggregate behavior, and save exactly the changed
aggregate. Missing source assets return an application-level `KnowledgeAssetNotFound`; repository
failures are not recast as domain validation errors. Acceptance/rejection reasons, command DTO
serialization, listing/searching, deletion, bulk operations, inverse traversal, and content editing
are not in BIT-466.

## Ports and module structure

Define one application-owned `KnowledgeAssetRepository` protocol with only `get(id) ->
KnowledgeAsset | None`, `exists(id) -> bool`, and `save(asset) -> None`. `exists` supports target and
create checks without prescribing queries; `save` covers creation and updates. Do not ship an
in-memory production adapter. Tests may provide a local fake. No Unit of Work, event bus, database,
filesystem, Git, web framework, dependency-injection framework, or concrete persistence adapter is
justified by these use cases.

The minimal intended structure is:

```text
src/rocky/
  knowledge_assets/
    __init__.py
    domain.py
    errors.py
    application.py
    ports.py
tests/
  knowledge_assets/
    test_values.py
    test_knowledge_asset.py
    test_application.py
  test_architecture.py
```

The domain imports only the Python standard library and domain errors. Application imports domain
and its owned port. Ports import domain types for signatures. Domain must not import application,
ports, repository tooling, frameworks, or adapters. Do not add speculative contexts, shared-kernel
packages, empty infrastructure directories, or one-file-per-class ceremony.

## Documentation and architecture status

BIT-466 must update [ARCH-001](../../../docs/architecture/ARCH-001.md) directly: this is the
smallest coherent change because it already owns capability status, the Knowledge Asset model, and
the dependency rule. Update factual runtime status and distinguish runtime behavior from the
repository documentation model; do not introduce another architecture asset. Update
[CAT-001](../../../docs/catalog/CAT-001.md) only enough to point to the implemented runtime package
and evidence. Do not claim implementation before code and tests exist, and do not accept proposed
documents without maintainer action.

## Explicit exclusions and deferrals

BIT-466 excludes runtime `Artifact`, Workspace, EngineeringProject, Repository runtime domain,
Workflow, Release, filesystem scanning, front-matter or Markdown parsing, persistence adapters,
database or graph selection, Git/Jira/GitHub/Confluence/Slack/SAP integrations, AI orchestration,
web API, UI, authentication, authorization, tenancy, and deployment topology. It also defers domain
events, timestamps/audit history, optimistic concurrency, deletion, content storage, relationship
graph queries, and automated inverse repair until concrete requirements justify them.

## Acceptance criteria

1. The aggregate and value objects enforce every boundary, normalization, equality, lifecycle,
   evolution, ownership, content-reference, and relationship rule specified above with explicit
   failures and no infrastructure dependency.
2. Every transition cell and series-policy constraint is tested; accepted evolution and explicit
   successor behavior cannot be bypassed through public state mutation.
3. Exactly the listed application use cases operate through the minimal abstract repository and
   are tested with test doubles, including missing sources/targets and duplicate creation.
4. Imports satisfy ARCH-001's inward rule; no excluded runtime type, adapter, framework, dependency,
   provider concept, speculative layer, or generic CRUD surface is introduced.
5. ARCH-001 and CAT-001 report only factual post-implementation status, navigation and links are
   coherent, and no storage/Git/Markdown assumptions enter the core.
6. Every automated gate and manual inspection in [TESTS](TESTS.md) is completed, with exact command
   evidence and unresolved findings recorded in [REVIEW](REVIEW.md).
