"""Application-owned persistence contract."""

from typing import Protocol

from .domain import KnowledgeAsset, KnowledgeAssetId


class KnowledgeAssetRepository(Protocol):
    def get(self, id: KnowledgeAssetId) -> KnowledgeAsset | None: ...
    def exists(self, id: KnowledgeAssetId) -> bool: ...
    def save(self, asset: KnowledgeAsset) -> None: ...
