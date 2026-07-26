"""Intention-revealing Knowledge Asset application operations."""

from .domain import (
    AssetRelationship,
    KnowledgeAsset,
    KnowledgeAssetId,
    KnowledgeAssetStatus,
    SeriesPolicy,
    SuccessorSummary,
)
from .errors import (
    InvalidLifecycleTransition,
    KnowledgeAssetAlreadyExists,
    KnowledgeAssetNotFound,
    RelationshipTargetNotFound,
)
from .ports import KnowledgeAssetRepository


def retrieve(repository: KnowledgeAssetRepository, id: KnowledgeAssetId) -> KnowledgeAsset:
    asset = repository.get(id)
    if asset is None:
        raise KnowledgeAssetNotFound("knowledge asset was not found", id.value)
    return asset


def create_draft(repository: KnowledgeAssetRepository, asset: KnowledgeAsset) -> None:
    if asset.status is not KnowledgeAssetStatus.DRAFT:
        raise InvalidLifecycleTransition("creation requires a draft", asset.status)
    if repository.exists(asset.id):
        raise KnowledgeAssetAlreadyExists("knowledge asset already exists", asset.id.value)
    repository.save(asset)


def _transition(
    repository: KnowledgeAssetRepository,
    id: KnowledgeAssetId,
    target: KnowledgeAssetStatus,
    policy: SeriesPolicy | None = None,
) -> KnowledgeAsset:
    asset = retrieve(repository, id)
    asset.transition(target, policy)
    repository.save(asset)
    return asset


def propose(
    repository: KnowledgeAssetRepository, id: KnowledgeAssetId, policy: SeriesPolicy | None = None
) -> KnowledgeAsset:
    return _transition(repository, id, KnowledgeAssetStatus.PROPOSED, policy)


def accept(
    repository: KnowledgeAssetRepository, id: KnowledgeAssetId, policy: SeriesPolicy | None = None
) -> KnowledgeAsset:
    return _transition(repository, id, KnowledgeAssetStatus.ACCEPTED, policy)


def reject(
    repository: KnowledgeAssetRepository, id: KnowledgeAssetId, policy: SeriesPolicy | None = None
) -> KnowledgeAsset:
    return _transition(repository, id, KnowledgeAssetStatus.REJECTED, policy)


def deprecate(
    repository: KnowledgeAssetRepository, id: KnowledgeAssetId, policy: SeriesPolicy | None = None
) -> KnowledgeAsset:
    return _transition(repository, id, KnowledgeAssetStatus.DEPRECATED, policy)


def archive(
    repository: KnowledgeAssetRepository, id: KnowledgeAssetId, policy: SeriesPolicy | None = None
) -> KnowledgeAsset:
    return _transition(repository, id, KnowledgeAssetStatus.ARCHIVED, policy)


def supersede(
    repository: KnowledgeAssetRepository,
    id: KnowledgeAssetId,
    successor_id: KnowledgeAssetId,
    policy: SeriesPolicy | None = None,
) -> KnowledgeAsset:
    asset = retrieve(repository, id)
    successor = repository.get(successor_id)
    if successor is None:
        raise RelationshipTargetNotFound("successor was not found", successor_id.value)
    asset.transition(
        KnowledgeAssetStatus.SUPERSEDED,
        policy,
        SuccessorSummary(successor.id, successor.kind, successor.status, successor.version),
    )
    repository.save(asset)
    return asset


def add_relationship(
    repository: KnowledgeAssetRepository, id: KnowledgeAssetId, relationship: AssetRelationship
) -> KnowledgeAsset:
    asset = retrieve(repository, id)
    if not repository.exists(relationship.target):
        raise RelationshipTargetNotFound(
            "relationship target was not found", relationship.target.value
        )
    asset.add_relationship(relationship)
    repository.save(asset)
    return asset


def remove_relationship(
    repository: KnowledgeAssetRepository, id: KnowledgeAssetId, relationship: AssetRelationship
) -> KnowledgeAsset:
    asset = retrieve(repository, id)
    asset.remove_relationship(relationship)
    repository.save(asset)
    return asset
