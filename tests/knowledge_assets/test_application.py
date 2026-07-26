import pytest

from rocky.knowledge_assets.application import (
    accept,
    add_relationship,
    archive,
    create_draft,
    deprecate,
    propose,
    reject,
    remove_relationship,
    retrieve,
    supersede,
)
from rocky.knowledge_assets.domain import (
    AssetRelationship,
    KnowledgeAsset,
    KnowledgeAssetId,
    KnowledgeAssetKind,
    Owner,
    SemanticVersion,
)
from rocky.knowledge_assets.domain import (
    KnowledgeAssetStatus as S,
)
from rocky.knowledge_assets.domain import (
    RelationshipType as R,
)
from rocky.knowledge_assets.errors import (
    KnowledgeAssetAlreadyExists,
    KnowledgeAssetNotFound,
    RelationshipTargetNotFound,
)


class Repo:
    def __init__(self, *assets: KnowledgeAsset) -> None:
        self.items = {a.id: a for a in assets}
        self.saved: list[KnowledgeAsset] = []

    def get(self, id: KnowledgeAssetId) -> KnowledgeAsset | None:
        return self.items.get(id)

    def exists(self, id: KnowledgeAssetId) -> bool:
        return id in self.items

    def save(self, a: KnowledgeAsset) -> None:
        self.items[a.id] = a
        self.saved.append(a)


def make(number: str = "001", status: S = S.DRAFT, version: str = "1.0.0") -> KnowledgeAsset:
    item = KnowledgeAsset(
        KnowledgeAssetId(f"ADR-{number}"),
        KnowledgeAssetKind.ADR,
        SemanticVersion(version),
        {Owner("Owner")},
    )
    if status is not S.DRAFT:
        item.transition(S.PROPOSED)
    if status is S.ACCEPTED:
        item.transition(S.ACCEPTED)
    return item


def test_create_retrieve_and_duplicate() -> None:
    repo = Repo()
    item = make()
    create_draft(repo, item)
    assert retrieve(repo, item.id) is item
    with pytest.raises(KnowledgeAssetAlreadyExists):
        create_draft(repo, item)
    with pytest.raises(KnowledgeAssetNotFound):
        retrieve(repo, KnowledgeAssetId("ADR-999"))


def test_lifecycle_use_cases_save_only_changed_source() -> None:
    item = make()
    repo = Repo(item)
    propose(repo, item.id)
    accept(repo, item.id)
    deprecate(repo, item.id)
    archive(repo, item.id)
    assert len(repo.saved) == 4
    rejected = make("002")
    repo = Repo(rejected)
    propose(repo, rejected.id)
    reject(repo, rejected.id)
    assert rejected.status is S.REJECTED


def test_supersede_requires_existing_accepted_successor() -> None:
    old = make(status=S.ACCEPTED)
    repo = Repo(old)
    with pytest.raises(RelationshipTargetNotFound):
        supersede(repo, old.id, KnowledgeAssetId("ADR-002"))
    assert not repo.saved
    successor = make("002", S.ACCEPTED, "2.0.0")
    repo.items[successor.id] = successor
    supersede(repo, old.id, successor.id)
    assert repo.saved == [old] and old.status is S.SUPERSEDED


def test_relationship_commands_check_target_and_save_source_only() -> None:
    source, target = make(), make("002")
    rel = AssetRelationship(R.REFERENCES, target.id)
    repo = Repo(source)
    with pytest.raises(RelationshipTargetNotFound):
        add_relationship(repo, source.id, rel)
    assert not repo.saved
    repo.items[target.id] = target
    add_relationship(repo, source.id, rel)
    remove_relationship(repo, source.id, rel)
    assert repo.saved == [source, source]


def test_repository_failures_propagate() -> None:
    class Broken(Repo):
        def get(self, id: KnowledgeAssetId) -> KnowledgeAsset | None:
            raise RuntimeError("storage failed")

    with pytest.raises(RuntimeError, match="storage failed"):
        retrieve(Broken(), KnowledgeAssetId("ADR-001"))
