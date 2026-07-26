"""Explicit handlers for Engagement commands and queries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from rocky.engagements.domain import (
    Actor,
    Decision,
    Engagement,
    EngagementId,
    Goal,
    Milestone,
    Participant,
)

from .commands import (
    AddParticipant,
    AssignOwner,
    CancelEngagement,
    CompleteEngagement,
    CompleteMilestone,
    CreateEngagement,
    RecordDecision,
    RegisterMilestone,
    RemoveParticipant,
    ResumeEngagement,
    StartEngagement,
    SuspendEngagement,
)
from .dto import EngagementView, to_engagement_view
from .errors import EngagementAlreadyExists, EngagementNotFound
from .ports import Clock, EngagementRepository
from .queries import GetEngagement

Mutation = Callable[[Engagement], None]


def _load(repository: EngagementRepository, raw_id: str) -> Engagement:
    engagement_id = EngagementId(raw_id)
    engagement = repository.get(engagement_id)
    if engagement is None:
        raise EngagementNotFound(raw_id)
    return engagement


def _mutate(
    repository: EngagementRepository,
    raw_id: str,
    operation: Mutation,
) -> EngagementView:
    engagement = _load(repository, raw_id)
    operation(engagement)
    repository.save(engagement)
    return to_engagement_view(engagement)


@dataclass(frozen=True, slots=True)
class CreateEngagementHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: CreateEngagement) -> EngagementView:
        engagement_id = EngagementId(command.engagement_id)
        if self.repository.get(engagement_id) is not None:
            raise EngagementAlreadyExists(command.engagement_id)
        moment = self.clock()
        engagement = Engagement.create(
            engagement_id=engagement_id,
            owner=Actor(command.owner_identifier, command.owner_display_name),
            goal=Goal(command.goal_title, command.goal_description),
            at=moment,
        )
        self.repository.add(engagement)
        return to_engagement_view(engagement)


@dataclass(frozen=True, slots=True)
class AssignOwnerHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: AssignOwner) -> EngagementView:
        moment = self.clock()
        owner = Actor(command.owner_identifier, command.owner_display_name)
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.assign_owner(owner, at=moment),
        )


@dataclass(frozen=True, slots=True)
class AddParticipantHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: AddParticipant) -> EngagementView:
        moment = self.clock()
        participant = Participant(
            actor=Actor(command.actor_identifier, command.actor_display_name),
            role=command.role,
        )
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.add_participant(participant, at=moment),
        )


@dataclass(frozen=True, slots=True)
class RemoveParticipantHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: RemoveParticipant) -> EngagementView:
        moment = self.clock()
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.remove_participant(
                command.actor_identifier,
                at=moment,
            ),
        )


@dataclass(frozen=True, slots=True)
class RecordDecisionHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: RecordDecision) -> EngagementView:
        moment = self.clock()
        decision = Decision(
            occurred_at=moment,
            author=Actor(command.author_identifier, command.author_display_name),
            rationale=command.rationale,
            outcome=command.outcome,
        )
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.record_decision(decision, at=moment),
        )


@dataclass(frozen=True, slots=True)
class RegisterMilestoneHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: RegisterMilestone) -> EngagementView:
        moment = self.clock()
        milestone = Milestone(command.milestone_identifier, command.milestone_name)
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.register_milestone(milestone, at=moment),
        )


@dataclass(frozen=True, slots=True)
class CompleteMilestoneHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: CompleteMilestone) -> EngagementView:
        moment = self.clock()
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.complete_milestone(
                command.milestone_identifier,
                at=moment,
            ),
        )


@dataclass(frozen=True, slots=True)
class StartEngagementHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: StartEngagement) -> EngagementView:
        moment = self.clock()
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.start(at=moment),
        )


@dataclass(frozen=True, slots=True)
class SuspendEngagementHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: SuspendEngagement) -> EngagementView:
        moment = self.clock()
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.suspend(at=moment),
        )


@dataclass(frozen=True, slots=True)
class ResumeEngagementHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: ResumeEngagement) -> EngagementView:
        moment = self.clock()
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.resume(at=moment),
        )


@dataclass(frozen=True, slots=True)
class CompleteEngagementHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: CompleteEngagement) -> EngagementView:
        moment = self.clock()
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.complete(at=moment),
        )


@dataclass(frozen=True, slots=True)
class CancelEngagementHandler:
    repository: EngagementRepository
    clock: Clock

    def handle(self, command: CancelEngagement) -> EngagementView:
        moment = self.clock()
        return _mutate(
            self.repository,
            command.engagement_id,
            lambda engagement: engagement.cancel(at=moment),
        )


@dataclass(frozen=True, slots=True)
class GetEngagementHandler:
    repository: EngagementRepository

    def handle(self, query: GetEngagement) -> EngagementView:
        return to_engagement_view(_load(self.repository, query.engagement_id))
