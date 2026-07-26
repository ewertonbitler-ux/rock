"""Persistence-free Knowledge Asset aggregate and value objects."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from functools import total_ordering
from types import MappingProxyType
from typing import ClassVar, Protocol

from .errors import (
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

_ID = re.compile(r"([A-Z]{2,16})-([0-9]{3,4})\Z", re.ASCII)
_PREFIX = re.compile(r"[A-Z]{2,16}\Z", re.ASCII)
_SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?\Z",
    re.ASCII,
)
_CONTENT = re.compile(r"([a-z][a-z0-9+.-]*):(.+)\Z", re.ASCII)


@dataclass(frozen=True, slots=True, init=False)
class KnowledgeAssetKind:
    name: str
    prefix: str
    _CANONICAL: ClassVar[dict[str, str]] = {
        "Product Charter": "RKY",
        "PRD": "PRD",
        "ADR": "ADR",
        "EPKG": "EPKG",
        "SPEC": "SPEC",
        "PROMPT": "PROMPT",
        "REVIEW": "REVIEW",
        "TESTS": "TESTS",
        "ARCH": "ARCH",
        "CAT": "CAT",
        "RFC": "RFC",
        "Pattern": "PAT",
        "Lesson Learned": "LL",
        "Postmortem": "PM",
        "Checklist": "CHECK",
        "Template": "TMPL",
    }
    RKY: ClassVar[KnowledgeAssetKind]
    PRD: ClassVar[KnowledgeAssetKind]
    ADR: ClassVar[KnowledgeAssetKind]
    EPKG: ClassVar[KnowledgeAssetKind]
    SPEC: ClassVar[KnowledgeAssetKind]
    PROMPT: ClassVar[KnowledgeAssetKind]
    REVIEW: ClassVar[KnowledgeAssetKind]
    TESTS: ClassVar[KnowledgeAssetKind]
    ARCH: ClassVar[KnowledgeAssetKind]
    CAT: ClassVar[KnowledgeAssetKind]
    RFC: ClassVar[KnowledgeAssetKind]
    PAT: ClassVar[KnowledgeAssetKind]
    LL: ClassVar[KnowledgeAssetKind]
    PM: ClassVar[KnowledgeAssetKind]
    CHECK: ClassVar[KnowledgeAssetKind]
    TMPL: ClassVar[KnowledgeAssetKind]

    def __init__(self, name: str, prefix: str) -> None:
        raise InvalidKnowledgeAssetKind(
            "additional kinds must be created with KnowledgeAssetKind.extension()",
            (name, prefix),
        )

    @classmethod
    def _create(cls, name: str, prefix: str) -> KnowledgeAssetKind:
        if (
            not name
            or name != name.strip()
            or any(unicodedata.category(c) == "Cc" for c in name)
            or not _PREFIX.fullmatch(prefix)
        ):
            raise InvalidKnowledgeAssetKind("invalid canonical kind name or prefix", (name, prefix))
        expected = cls._CANONICAL.get(name)
        if expected is not None and expected != prefix:
            raise InvalidKnowledgeAssetKind("canonical name has a different prefix", name)
        owner = next((item for item, value in cls._CANONICAL.items() if value == prefix), None)
        if owner is not None and owner != name:
            raise InvalidKnowledgeAssetKind("canonical prefix is already claimed", prefix)
        kind = object.__new__(cls)
        object.__setattr__(kind, "name", name)
        object.__setattr__(kind, "prefix", prefix)
        return kind

    @classmethod
    def extension(
        cls, name: str, prefix: str, claimed: Iterable[KnowledgeAssetKind] = ()
    ) -> KnowledgeAssetKind:
        kind = cls._create(name, prefix)
        if any(existing.prefix == prefix and existing != kind for existing in claimed):
            raise InvalidKnowledgeAssetKind("extension prefix is already claimed", prefix)
        return kind


for _name, _prefix in KnowledgeAssetKind._CANONICAL.items():
    setattr(KnowledgeAssetKind, _prefix, KnowledgeAssetKind._create(_name, _prefix))


@dataclass(frozen=True, slots=True)
class KnowledgeAssetId:
    value: str

    def __post_init__(self) -> None:
        if not _ID.fullmatch(self.value):
            raise InvalidKnowledgeAssetId(
                "ID must use canonical KIND-NNN or KIND-NNNN form", self.value
            )

    @property
    def prefix(self) -> str:
        return self.value.split("-", 1)[0]

    def __str__(self) -> str:
        return self.value


@total_ordering
@dataclass(frozen=True, slots=True)
class SemanticVersion:
    value: str

    def __post_init__(self) -> None:
        if not _SEMVER.fullmatch(self.value):
            raise InvalidSemanticVersion("version must be canonical SemVer 2.0.0", self.value)

    def _precedence(self) -> tuple[int, int, int, tuple[tuple[int, int | str], ...] | None]:
        match = _SEMVER.fullmatch(self.value)
        assert match is not None
        pre = match.group(4)
        parts = (
            None
            if pre is None
            else tuple((0, int(p)) if p.isdigit() else (1, p) for p in pre.split("."))
        )
        return int(match.group(1)), int(match.group(2)), int(match.group(3)), parts

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        left, right = self._precedence(), other._precedence()
        if left[:3] != right[:3]:
            return left[:3] < right[:3]
        if left[3] is None:
            return False
        if right[3] is None:
            return True
        for a, b in zip(left[3], right[3]):
            if a == b:
                continue
            if a[0] != b[0]:
                return a[0] < b[0]
            if isinstance(a[1], int) and isinstance(b[1], int):
                return a[1] < b[1]
            if isinstance(a[1], str) and isinstance(b[1], str):
                return a[1] < b[1]
            raise AssertionError("prerelease identifiers have inconsistent types")
        return len(left[3]) < len(right[3])


@dataclass(frozen=True, slots=True)
class Owner:
    value: str
    _key: str = ""

    def __post_init__(self) -> None:
        normalized = unicodedata.normalize("NFC", " ".join(self.value.split()))
        if (
            not normalized
            or len(normalized) > 200
            or any(unicodedata.category(c) == "Cc" for c in normalized)
        ):
            raise InvalidOwner(
                "owner must be a non-empty accountable label of at most 200 code points", self.value
            )
        object.__setattr__(self, "value", normalized)
        object.__setattr__(self, "_key", normalized.casefold())

    def __hash__(self) -> int:
        return hash(self._key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Owner) and self._key == other._key


@dataclass(frozen=True, slots=True)
class ContentReference:
    value: str

    def __post_init__(self) -> None:
        match = _CONTENT.fullmatch(self.value)
        body = match.group(2) if match else ""
        if (
            not match
            or body != body.strip()
            or len(body) > 500
            or any(c.isspace() or unicodedata.category(c) == "Cc" for c in body)
        ):
            raise InvalidContentReference(
                "content reference must be an opaque scheme:value key", self.value
            )

    @property
    def scheme(self) -> str:
        return self.value.split(":", 1)[0]


class KnowledgeAssetStatus(StrEnum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class RelationshipType(StrEnum):
    GOVERNS = "governs"
    GOVERNED_BY = "governed-by"
    SUPERSEDES = "supersedes"
    SUPERSEDED_BY = "superseded-by"
    PACKAGES = "packages"
    PACKAGED_BY = "packaged-by"
    REFERENCES = "references"
    REFERENCED_BY = "referenced-by"
    IMPLEMENTS = "implements"
    IMPLEMENTED_BY = "implemented-by"
    VALIDATES = "validates"
    VALIDATED_BY = "validated-by"

    @property
    def inverse(self) -> RelationshipType:
        return _RELATIONSHIP_INVERSES[self]


_RELATIONSHIP_INVERSES = MappingProxyType(
    {
        RelationshipType.GOVERNS: RelationshipType.GOVERNED_BY,
        RelationshipType.GOVERNED_BY: RelationshipType.GOVERNS,
        RelationshipType.SUPERSEDES: RelationshipType.SUPERSEDED_BY,
        RelationshipType.SUPERSEDED_BY: RelationshipType.SUPERSEDES,
        RelationshipType.PACKAGES: RelationshipType.PACKAGED_BY,
        RelationshipType.PACKAGED_BY: RelationshipType.PACKAGES,
        RelationshipType.REFERENCES: RelationshipType.REFERENCED_BY,
        RelationshipType.REFERENCED_BY: RelationshipType.REFERENCES,
        RelationshipType.IMPLEMENTS: RelationshipType.IMPLEMENTED_BY,
        RelationshipType.IMPLEMENTED_BY: RelationshipType.IMPLEMENTS,
        RelationshipType.VALIDATES: RelationshipType.VALIDATED_BY,
        RelationshipType.VALIDATED_BY: RelationshipType.VALIDATES,
    }
)


@dataclass(frozen=True, slots=True)
class AssetRelationship:
    type: RelationshipType
    target: KnowledgeAssetId

    def __post_init__(self) -> None:
        if not isinstance(self.type, RelationshipType) or not isinstance(
            self.target, KnowledgeAssetId
        ):
            raise InvalidRelationship(
                "relationship requires a type and target ID", (self.type, self.target)
            )


@dataclass(frozen=True, slots=True)
class SuccessorSummary:
    id: KnowledgeAssetId
    kind: KnowledgeAssetKind
    status: KnowledgeAssetStatus
    version: SemanticVersion


class SeriesPolicy(Protocol):
    def permits(self, asset: KnowledgeAsset, target: KnowledgeAssetStatus) -> bool: ...


_TRANSITIONS = MappingProxyType(
    {
        KnowledgeAssetStatus.DRAFT: frozenset(
            {KnowledgeAssetStatus.PROPOSED, KnowledgeAssetStatus.ARCHIVED}
        ),
        KnowledgeAssetStatus.PROPOSED: frozenset(
            {
                KnowledgeAssetStatus.ACCEPTED,
                KnowledgeAssetStatus.REJECTED,
                KnowledgeAssetStatus.ARCHIVED,
            }
        ),
        KnowledgeAssetStatus.ACCEPTED: frozenset(
            {
                KnowledgeAssetStatus.SUPERSEDED,
                KnowledgeAssetStatus.DEPRECATED,
                KnowledgeAssetStatus.ARCHIVED,
            }
        ),
        KnowledgeAssetStatus.REJECTED: frozenset({KnowledgeAssetStatus.ARCHIVED}),
        KnowledgeAssetStatus.SUPERSEDED: frozenset(
            {
                KnowledgeAssetStatus.DEPRECATED,
                KnowledgeAssetStatus.ARCHIVED,
            }
        ),
        KnowledgeAssetStatus.DEPRECATED: frozenset({KnowledgeAssetStatus.ARCHIVED}),
        KnowledgeAssetStatus.ARCHIVED: frozenset(),
    }
)


class KnowledgeAsset:
    def __init__(
        self,
        id: KnowledgeAssetId,
        kind: KnowledgeAssetKind,
        version: SemanticVersion,
        owners: set[Owner] | frozenset[Owner],
        content_reference: ContentReference | None = None,
    ) -> None:
        if not isinstance(id, KnowledgeAssetId):
            raise InvalidKnowledgeAssetId("asset ID must be a KnowledgeAssetId", id)
        if not isinstance(kind, KnowledgeAssetKind):
            raise InvalidKnowledgeAssetKind("asset kind must be a KnowledgeAssetKind", kind)
        if not isinstance(version, SemanticVersion):
            raise InvalidSemanticVersion("asset version must be a SemanticVersion", version)
        if not isinstance(owners, (set, frozenset)) or any(
            not isinstance(owner, Owner) for owner in owners
        ):
            raise InvalidOwner("asset owners must be a set of Owner values", owners)
        if content_reference is not None and not isinstance(content_reference, ContentReference):
            raise InvalidContentReference(
                "asset content reference must be ContentReference or None", content_reference
            )
        if id.prefix != kind.prefix:
            raise KindIdentifierMismatch("ID prefix does not match kind", id.value)
        if not owners:
            raise LastOwnerRemoval("an asset requires at least one owner", id.value)
        self._id, self._kind, self._version = id, kind, version
        self._status = KnowledgeAssetStatus.DRAFT
        self._owners, self._content_reference = set(owners), content_reference
        self._relationships: set[AssetRelationship] = set()

    id = property(lambda s: s._id)
    kind = property(lambda s: s._kind)
    version = property(lambda s: s._version)
    status = property(lambda s: s._status)
    owners = property(lambda s: frozenset(s._owners))
    content_reference = property(lambda s: s._content_reference)
    relationships = property(lambda s: frozenset(s._relationships))

    def transition(
        self,
        target: KnowledgeAssetStatus,
        policy: SeriesPolicy | None = None,
        successor: SuccessorSummary | None = None,
    ) -> None:
        if target not in _TRANSITIONS[self._status]:
            raise InvalidLifecycleTransition(
                f"cannot transition {self._status.value} to {target.value}", target
            )
        if policy is not None and not policy.permits(self, target):
            raise SeriesPolicyViolation("series policy rejected transition", target)
        if target is KnowledgeAssetStatus.SUPERSEDED:
            if successor is None:
                raise SuccessorRequired("supersession requires a successor", self.id.value)
            if (
                successor.id == self.id
                or successor.kind != self.kind
                or successor.status is not KnowledgeAssetStatus.ACCEPTED
                or not self.version < successor.version
            ):
                raise InvalidSuccessor(
                    "successor must be distinct, accepted, same-kind, and newer", successor.id.value
                )
            relationship = AssetRelationship(RelationshipType.SUPERSEDED_BY, successor.id)
            if relationship in self._relationships:
                raise DuplicateRelationship(
                    "supersession relationship already exists", relationship
                )
            self._relationships.add(relationship)
        self._status = target

    def change_version(self, version: SemanticVersion) -> None:
        if self.status not in {KnowledgeAssetStatus.DRAFT, KnowledgeAssetStatus.PROPOSED}:
            if self.status is KnowledgeAssetStatus.ACCEPTED:
                raise ImmutableAcceptedAsset("accepted assets cannot change version", self.id.value)
            raise VersionRegression("version cannot change in this lifecycle state", self.status)
        if not self.version < version:
            raise VersionRegression("new version must have greater precedence", version.value)
        self._version = version

    def add_owner(self, owner: Owner) -> None:
        if owner in self._owners:
            raise DuplicateOwner("equivalent owner already exists", owner.value)
        self._owners.add(owner)

    def remove_owner(self, owner: Owner) -> None:
        if owner not in self._owners:
            raise InvalidOwner("owner is not assigned", owner.value)
        if len(self._owners) == 1:
            raise LastOwnerRemoval("cannot remove the last owner", owner.value)
        self._owners.remove(owner)

    def add_relationship(self, relationship: AssetRelationship) -> None:
        if relationship.target == self.id:
            raise InvalidRelationship("self relationships are forbidden", self.id.value)
        if relationship in self._relationships:
            raise DuplicateRelationship("relationship already exists", relationship)
        self._relationships.add(relationship)

    def remove_relationship(self, relationship: AssetRelationship) -> None:
        if relationship not in self._relationships:
            raise RelationshipNotFound("relationship does not exist", relationship)
        self._relationships.remove(relationship)
