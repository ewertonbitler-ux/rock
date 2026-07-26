"""Persistence-free Engagement aggregate."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Final

from .errors import (
    CompletedMilestoneImmutable,
    DuplicateMilestone,
    DuplicateParticipant,
    InvalidActor,
    InvalidDecision,
    InvalidEngagementId,
    InvalidGoal,
    InvalidLifecycleTransition,
    InvalidMilestone,
    MilestoneNotFound,
    OwnerCannotBeParticipant,
    ParticipantNotFound,
)

_ID_PATTERN: Final = re.compile(r"ENG-[0-9]{4}\Z", re.ASCII)


def _text(value: str, *, maximum: int, error: type[Exception], label: str) -> str:
    normalized = unicodedata.normalize("NFC", " ".join(value.split()))
    if not normalized or len(normalized) > maximum or any(
        unicodedata.category(char) == "Cc" for char in normalized
    ):
        raise error(f"invalid {label}")
    return normalized


@dataclass(frozen=True, slots=True)
class EngagementId:
    value: str

    def __post_init__(self) -> None:
        if not _ID_PATTERN.fullmatch(self.value):
            raise InvalidEngagementId("expected canonical ENG-0000 identifier")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Actor:
    identifier: str
    display_name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "identifier", _text(self.identifier, maximum=200, error=InvalidActor, label="actor identifier"))
        object.__setattr__(self, "display_name", _text(self.display_name, maximum=200, error=InvalidActor, label="actor display name"))

    @property
    def key(self) -> str:
        return self.identifier.casefold()


@dataclass(frozen=True, slots=True)
class Participant:
    actor: Actor
    role: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "role", _text(self.role, maximum=100, error=InvalidActor, label="participant role"))


@dataclass(frozen=True, slots=True)
class Goal:
    title: str
    description: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "title", _text(self.title, maximum=200, error=InvalidGoal, label="goal title"))
        object.__setattr__(self, "description", _text(self.description, maximum=4000, error=InvalidGoal, label="goal description"))


@dataclass(frozen=True, slots=True)
class Decision:
    occurred_at: datetime
    author: Actor
    rationale: str
    outcome: str

    def __post_init__(self) -> None:
        if self.occurred_at.tzinfo is None:
            raise InvalidDecision("decision timestamp must be timezone-aware")
        object.__setattr__(self, "rationale", _text(self.rationale, maximum=4000, error=InvalidDecision, label="decision rationale"))
        object.__setattr__(self, "outcome", _text(self.outcome, maximum=4000, error=InvalidDecision, label="decision outcome"))


class EngagementStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MilestoneStatus(StrEnum):
    PLANNED = "planned"
    COMPLETED = "completed"


@dataclass(slots=True)
class Milestone:
    identifier: str
    name: str
    status: MilestoneStatus = MilestoneStatus.PLANNED
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        self.identifier = _text(self.identifier, maximum=100, error=InvalidMilestone, label="milestone identifier")
        self.name = _text(self.name, maximum=200, error=InvalidMilestone, label="milestone name")

    def complete(self, at: datetime) -> None:
        if self.status is MilestoneStatus.COMPLETED:
            raise CompletedMilestoneImmutable("milestone is already completed")
        if at.tzinfo is None:
            raise InvalidMilestone("completion timestamp must be timezone-aware")
        self.status = MilestoneStatus.COMPLETED
        self.completed_at = at


@dataclass(slots=True)
class Engagement:
    engagement_id: EngagementId
    owner: Actor
    goal: Goal
    status: EngagementStatus = EngagementStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    _participants: dict[str, Participant] = field(default_factory=dict, repr=False)
    _decisions: list[Decision] = field(default_factory=list, repr=False)
    _milestones: dict[str, Milestone] = field(default_factory=dict, repr=False)

    @classmethod
    def create(cls, engagement_id: EngagementId, owner: Actor, goal: Goal, *, at: datetime | None = None) -> Engagement:
        moment = at or datetime.now(UTC)
        if moment.tzinfo is None:
            raise InvalidLifecycleTransition("creation timestamp must be timezone-aware")
        return cls(engagement_id=engagement_id, owner=owner, goal=goal, created_at=moment, updated_at=moment)

    @property
    def participants(self) -> tuple[Participant, ...]:
        return tuple(self._participants.values())

    @property
    def decisions(self) -> tuple[Decision, ...]:
        return tuple(self._decisions)

    @property
    def milestones(self) -> tuple[Milestone, ...]:
        return tuple(self._milestones.values())

    def assign_owner(self, owner: Actor, *, at: datetime | None = None) -> None:
        self._ensure_open()
        if owner.key in self._participants:
            raise OwnerCannotBeParticipant("owner cannot also be a participant")
        self.owner = owner
        self._touch(at)

    def add_participant(self, participant: Participant, *, at: datetime | None = None) -> None:
        self._ensure_open()
        if participant.actor.key == self.owner.key:
            raise OwnerCannotBeParticipant("owner cannot also be a participant")
        if participant.actor.key in self._participants:
            raise DuplicateParticipant(participant.actor.identifier)
        self._participants[participant.actor.key] = participant
        self._touch(at)

    def remove_participant(self, actor_identifier: str, *, at: datetime | None = None) -> None:
        self._ensure_open()
        key = actor_identifier.casefold()
        if key not in self._participants:
            raise ParticipantNotFound(actor_identifier)
        del self._participants[key]
        self._touch(at)

    def record_decision(self, decision: Decision, *, at: datetime | None = None) -> None:
        self._ensure_open()
        self._decisions.append(decision)
        self._touch(at)

    def register_milestone(self, milestone: Milestone, *, at: datetime | None = None) -> None:
        self._ensure_open()
        key = milestone.identifier.casefold()
        if key in self._milestones:
            raise DuplicateMilestone(milestone.identifier)
        self._milestones[key] = milestone
        self._touch(at)

    def complete_milestone(self, identifier: str, *, at: datetime | None = None) -> None:
        self._ensure_open()
        milestone = self._milestones.get(identifier.casefold())
        if milestone is None:
            raise MilestoneNotFound(identifier)
        moment = at or datetime.now(UTC)
        milestone.complete(moment)
        self.updated_at = moment

    def start(self, *, at: datetime | None = None) -> None:
        self._transition(EngagementStatus.ACTIVE, {EngagementStatus.DRAFT}, at)

    def suspend(self, *, at: datetime | None = None) -> None:
        self._transition(EngagementStatus.SUSPENDED, {EngagementStatus.ACTIVE}, at)

    def resume(self, *, at: datetime | None = None) -> None:
        self._transition(EngagementStatus.ACTIVE, {EngagementStatus.SUSPENDED}, at)

    def complete(self, *, at: datetime | None = None) -> None:
        self._transition(EngagementStatus.COMPLETED, {EngagementStatus.ACTIVE}, at)

    def cancel(self, *, at: datetime | None = None) -> None:
        self._transition(EngagementStatus.CANCELLED, {EngagementStatus.DRAFT, EngagementStatus.ACTIVE, EngagementStatus.SUSPENDED}, at)

    def _transition(self, target: EngagementStatus, allowed: set[EngagementStatus], at: datetime | None) -> None:
        if self.status not in allowed:
            raise InvalidLifecycleTransition(f"cannot transition from {self.status} to {target}")
        self.status = target
        self._touch(at)

    def _ensure_open(self) -> None:
        if self.status in {EngagementStatus.COMPLETED, EngagementStatus.CANCELLED}:
            raise InvalidLifecycleTransition(f"engagement is terminal: {self.status}")

    def _touch(self, at: datetime | None) -> None:
        moment = at or datetime.now(UTC)
        if moment.tzinfo is None:
            raise InvalidLifecycleTransition("timestamp must be timezone-aware")
        self.updated_at = moment
