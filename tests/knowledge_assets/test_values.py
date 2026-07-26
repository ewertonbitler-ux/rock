import pytest

from rocky.knowledge_assets.domain import (
    ContentReference,
    KnowledgeAssetId,
    KnowledgeAssetKind,
    Owner,
    RelationshipType,
    SemanticVersion,
)
from rocky.knowledge_assets.errors import (
    InvalidContentReference,
    InvalidKnowledgeAssetId,
    InvalidKnowledgeAssetKind,
    InvalidOwner,
    InvalidSemanticVersion,
)


@pytest.mark.parametrize("value", ["ADR-001", "EPKG-0003", "RKY-000"])
def test_ids_accept_canonical_values(value: str) -> None:
    assert str(KnowledgeAssetId(value)) == value


@pytest.mark.parametrize("value", ["adr-001", "ADR-1", "ADR-00001", "ADR_001", "A-001", " ADR-001"])
def test_ids_reject_noncanonical_values(value: str) -> None:
    with pytest.raises(InvalidKnowledgeAssetId):
        KnowledgeAssetId(value)


def test_kinds_are_typed_open_values_without_global_registration() -> None:
    assert (KnowledgeAssetKind.ADR.name, KnowledgeAssetKind.ADR.prefix) == ("ADR", "ADR")
    guide = KnowledgeAssetKind.extension("Guide", "GUIDE")
    assert (guide.name, guide.prefix) == ("Guide", "GUIDE")
    with pytest.raises(InvalidKnowledgeAssetKind):
        KnowledgeAssetKind.extension("Manual", "GUIDE", [guide])
    with pytest.raises(InvalidKnowledgeAssetKind):
        KnowledgeAssetKind.extension("ADR", "OTHER")
    with pytest.raises(InvalidKnowledgeAssetKind):
        KnowledgeAssetKind.extension("Other", "ADR")
    with pytest.raises(InvalidKnowledgeAssetKind):
        KnowledgeAssetKind("Guide", "GUIDE")
    with pytest.raises(InvalidKnowledgeAssetKind):
        KnowledgeAssetKind("Other", "ADR")


@pytest.mark.parametrize("value", ["1.0.0", "1.2.3-alpha.1+build.5", "0.0.0"])
def test_semver_accepts_canonical_values(value: str) -> None:
    SemanticVersion(value)


@pytest.mark.parametrize("value", ["v1.0.0", "1.0", "01.0.0", "1.0.0-01", "1.0.0 ", "1.0.0-β"])
def test_semver_rejects_noncanonical_values(value: str) -> None:
    with pytest.raises(InvalidSemanticVersion):
        SemanticVersion(value)


def test_semver_precedence_ignores_build_but_equality_does_not() -> None:
    assert not SemanticVersion("1.0.0+one") < SemanticVersion("1.0.0+two")
    assert SemanticVersion("1.0.0+one") != SemanticVersion("1.0.0+two")
    assert SemanticVersion("1.0.0-alpha") < SemanticVersion("1.0.0")


def test_owner_normalizes_and_compares_by_casefolded_value() -> None:
    assert Owner("  Rocky\tMaintainers ") == Owner("rocky maintainers")
    assert Owner("  Rocky\tMaintainers ").value == "Rocky Maintainers"
    assert len({Owner("Straße"), Owner("STRASSE")}) == 1
    with pytest.raises(InvalidOwner):
        Owner(" \t")


def test_content_reference_is_opaque_and_validated() -> None:
    assert ContentReference("repo-key:ADR-001").scheme == "repo-key"
    for value in ["HTTP:x", "scheme:", "scheme: padded", " scheme:x"]:
        with pytest.raises(InvalidContentReference):
            ContentReference(value)


def test_relationship_inverse_is_derived() -> None:
    assert RelationshipType.GOVERNS.inverse is RelationshipType.GOVERNED_BY
    assert RelationshipType.VALIDATED_BY.inverse is RelationshipType.VALIDATES
