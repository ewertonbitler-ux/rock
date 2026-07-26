"""Explicit failures exposed by the knowledge-asset domain."""


class KnowledgeAssetError(Exception):
    """Base class for knowledge-asset validation and behavior failures."""

    def __init__(self, message: str, value: object | None = None) -> None:
        super().__init__(message)
        self.value = value


class InvalidKnowledgeAssetId(KnowledgeAssetError):
    pass


class InvalidKnowledgeAssetKind(KnowledgeAssetError):
    pass


class KindIdentifierMismatch(KnowledgeAssetError):
    pass


class InvalidSemanticVersion(KnowledgeAssetError):
    pass


class VersionRegression(KnowledgeAssetError):
    pass


class ImmutableAcceptedAsset(KnowledgeAssetError):
    pass


class InvalidOwner(KnowledgeAssetError):
    pass


class DuplicateOwner(KnowledgeAssetError):
    pass


class LastOwnerRemoval(KnowledgeAssetError):
    pass


class InvalidContentReference(KnowledgeAssetError):
    pass


class InvalidLifecycleTransition(KnowledgeAssetError):
    pass


class SuccessorRequired(KnowledgeAssetError):
    pass


class InvalidSuccessor(KnowledgeAssetError):
    pass


class InvalidRelationship(KnowledgeAssetError):
    pass


class DuplicateRelationship(KnowledgeAssetError):
    pass


class RelationshipNotFound(KnowledgeAssetError):
    pass


class RelationshipTargetNotFound(KnowledgeAssetError):
    pass


class SeriesPolicyViolation(KnowledgeAssetError):
    pass


class KnowledgeAssetNotFound(KnowledgeAssetError):
    pass


class KnowledgeAssetAlreadyExists(KnowledgeAssetError):
    pass
