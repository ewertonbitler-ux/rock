import pytest

from rocky.knowledge_assets.domain import (
    AssetRelationship,
    KnowledgeAsset,
    KnowledgeAssetId,
    KnowledgeAssetKind,
    Owner,
    SemanticVersion,
    SuccessorSummary,
)
from rocky.knowledge_assets.domain import (
    KnowledgeAssetStatus as S,
)
from rocky.knowledge_assets.domain import (
    RelationshipType as R,
)
from rocky.knowledge_assets.errors import (
    DuplicateOwner,
    DuplicateRelationship,
    ImmutableAcceptedAsset,
    InvalidContentReference,
    InvalidKnowledgeAssetId,
    InvalidKnowledgeAssetKind,
    InvalidLifecycleTransition,
    InvalidOwner,
    InvalidRelationship,
    InvalidSemanticVersion,
    InvalidSuccessor,
    KindIdentifierMismatch,
    LastOwnerRemoval,
    RelationshipNotFound,
    SeriesPolicyViolation,
    SuccessorRequired,
    VersionRegression,
)


def asset(status: S = S.DRAFT, number: str = "001", version: str = "1.0.0") -> KnowledgeAsset:
    item = KnowledgeAsset(
        KnowledgeAssetId(f"ADR-{number}"),
        KnowledgeAssetKind.ADR,
        SemanticVersion(version),
        {Owner("Rocky maintainers")},
    )
    if status is S.DRAFT:
        return item
    if status is S.ARCHIVED:
        item.transition(S.ARCHIVED)
        return item
    item.transition(S.PROPOSED)
    if status is S.PROPOSED:
        return item
    if status is S.REJECTED:
        item.transition(S.REJECTED)
        return item
    item.transition(S.ACCEPTED)
    if status is S.ACCEPTED:
        return item
    if status is S.SUPERSEDED:
        successor = asset(S.ACCEPTED, "999", "2.0.0")
        item.transition(
            S.SUPERSEDED,
            successor=SuccessorSummary(
                successor.id, successor.kind, successor.status, successor.version
            ),
        )
        return item
    item.transition(S.DEPRECATED)
    return item


VALID = {
    S.DRAFT: {S.PROPOSED, S.ARCHIVED},
    S.PROPOSED: {S.ACCEPTED, S.REJECTED, S.ARCHIVED},
    S.ACCEPTED: {S.SUPERSEDED, S.DEPRECATED, S.ARCHIVED},
    S.REJECTED: {S.ARCHIVED},
    S.SUPERSEDED: {S.DEPRECATED, S.ARCHIVED},
    S.DEPRECATED: {S.ARCHIVED},
    S.ARCHIVED: set(),
}


@pytest.mark.parametrize(("source", "target"), [(a, b) for a in S for b in S])
def test_complete_transition_matrix(source: S, target: S) -> None:
    item = asset(source)
    if target in VALID[source] and target is not S.SUPERSEDED:
        item.transition(target)
        assert item.status is target
    elif target is S.SUPERSEDED and source is S.ACCEPTED:
        successor = SuccessorSummary(
            KnowledgeAssetId("ADR-002"),
            KnowledgeAssetKind.ADR,
            S.ACCEPTED,
            SemanticVersion("2.0.0"),
        )
        item.transition(target, successor=successor)
        assert item.status is target
    else:
        with pytest.raises(InvalidLifecycleTransition):
            item.transition(target)


def test_kind_id_and_owner_construction_invariants() -> None:
    with pytest.raises(KindIdentifierMismatch):
        KnowledgeAsset(
            KnowledgeAssetId("PRD-001"),
            KnowledgeAssetKind.ADR,
            SemanticVersion("1.0.0"),
            {Owner("x")},
        )
    with pytest.raises(LastOwnerRemoval):
        KnowledgeAsset(
            KnowledgeAssetId("ADR-001"), KnowledgeAssetKind.ADR, SemanticVersion("1.0.0"), set()
        )


def test_constructor_creates_only_drafts_and_validates_argument_types() -> None:
    assert asset().status is S.DRAFT
    with pytest.raises(TypeError):
        KnowledgeAsset(  # type: ignore[call-arg]
            KnowledgeAssetId("ADR-001"),
            KnowledgeAssetKind.ADR,
            SemanticVersion("1.0.0"),
            {Owner("Owner")},
            status=S.ACCEPTED,
        )
    invalid_cases = [
        (
            "ADR-001",
            KnowledgeAssetKind.ADR,
            SemanticVersion("1.0.0"),
            {Owner("Owner")},
            None,
            InvalidKnowledgeAssetId,
        ),
        (
            KnowledgeAssetId("ADR-001"),
            "ADR",
            SemanticVersion("1.0.0"),
            {Owner("Owner")},
            None,
            InvalidKnowledgeAssetKind,
        ),
        (
            KnowledgeAssetId("ADR-001"),
            KnowledgeAssetKind.ADR,
            "1.0.0",
            {Owner("Owner")},
            None,
            InvalidSemanticVersion,
        ),
        (
            KnowledgeAssetId("ADR-001"),
            KnowledgeAssetKind.ADR,
            SemanticVersion("1.0.0"),
            {"Owner"},
            None,
            InvalidOwner,
        ),
        (
            KnowledgeAssetId("ADR-001"),
            KnowledgeAssetKind.ADR,
            SemanticVersion("1.0.0"),
            {Owner("Owner")},
            "key:value",
            InvalidContentReference,
        ),
    ]
    for id, kind, version, owners, reference, error in invalid_cases:
        with pytest.raises(error):
            KnowledgeAsset(id, kind, version, owners, reference)  # type: ignore[arg-type]


def test_state_collections_are_read_only_snapshots() -> None:
    item = asset()
    owners = item.owners
    assert isinstance(owners, frozenset)
    with pytest.raises(AttributeError):
        item.id = KnowledgeAssetId("ADR-002")


def test_version_evolution_is_explicit_and_increasing() -> None:
    item = asset()
    item.change_version(SemanticVersion("1.1.0"))
    assert item.version == SemanticVersion("1.1.0")
    with pytest.raises(VersionRegression):
        item.change_version(SemanticVersion("1.1.0+build"))
    accepted = asset(S.ACCEPTED)
    with pytest.raises(ImmutableAcceptedAsset):
        accepted.change_version(SemanticVersion("2.0.0"))


def test_owners_are_protected() -> None:
    item = asset()
    item.add_owner(Owner("Other"))
    with pytest.raises(DuplicateOwner):
        item.add_owner(Owner("OTHER"))
    item.remove_owner(Owner("other"))
    with pytest.raises(LastOwnerRemoval):
        item.remove_owner(Owner("ROCKY MAINTAINERS"))


def test_relationships_are_outbound_exact_and_protected() -> None:
    item = asset()
    target = KnowledgeAssetId("ADR-002")
    first = AssetRelationship(R.REFERENCES, target)
    second = AssetRelationship(R.IMPLEMENTS, target)
    item.add_relationship(first)
    item.add_relationship(second)
    assert (
        len(item.relationships) == 2
        and AssetRelationship(R.REFERENCED_BY, target) not in item.relationships
    )
    with pytest.raises(DuplicateRelationship):
        item.add_relationship(first)
    with pytest.raises(InvalidRelationship):
        item.add_relationship(AssetRelationship(R.GOVERNS, item.id))
    with pytest.raises(RelationshipNotFound):
        item.remove_relationship(AssetRelationship(R.PACKAGES, target))
    item.remove_relationship(first)


def test_supersession_requires_valid_explicit_successor_and_is_atomic() -> None:
    item = asset(S.ACCEPTED)
    with pytest.raises(SuccessorRequired):
        item.transition(S.SUPERSEDED)
    bad = SuccessorSummary(item.id, item.kind, S.ACCEPTED, SemanticVersion("2.0.0"))
    with pytest.raises(InvalidSuccessor):
        item.transition(S.SUPERSEDED, successor=bad)
    assert item.status is S.ACCEPTED and not item.relationships


def test_policy_can_restrict_but_cannot_relax_matrix() -> None:
    class Never:
        def permits(self, asset: KnowledgeAsset, target: S) -> bool:
            return False

    with pytest.raises(SeriesPolicyViolation):
        asset().transition(S.PROPOSED, Never())
    with pytest.raises(InvalidLifecycleTransition):
        asset(S.ARCHIVED).transition(S.DRAFT, Never())
