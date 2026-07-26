"""Immutable result DTOs for Engagement application use cases."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from rocky.engagements.domain import (
    Actor,
    Decision,
    Engagement,
    EngagementStatus,
    Goal,
    Milestone,
    MilestoneStatus,
    Participant,
)


@dataclass(frozen=True, slots=True)
class ActorView:
    identifier: str
    display_name: str


@dataclass(frozen=True, slots=True)
class ParticipantView:
    actor: ActorView
    role: str


@dataclass(frozen=True, slots=True)
class GoalView:
    title: str
    description: str


@dataclass(frozen=True, slots=True)
class DecisionView:
    occurred_at: datetime
    author: ActorView
    rationale: str
    outcome: str


@dataclass(frozen=True, slots=True)
class MilestoneView:
    identifier: str
    name: str
    status: MilestoneStatus
    completed_at: datetime | None


@dataclass(frozen=True, slots=True)
class EngagementView:
    engagement_id: str
    owner: ActorView
    goal: GoalView
    status: EngagementStatus
    created_at: datetime
    updated_at: datetime
    participants: tuple[ParticipantView, ...]
    decisions: tuple[DecisionView, ...]
    milestones: tuple[MilestoneView, ...]


def _actor_view(actor: Actor) -> ActorView:
    return ActorView(identifier=actor.identifier, display_name=actor.display_name)


def _participant_view(participant: Participant) -> ParticipantView:
    return ParticipantView(actor=_actor_view(participant.actor), role=participant.role)


def _goal_view(goal: Goal) -> GoalView:
    return GoalView(title=goal.title, description=goal.description)


def _decision_view(decision: Decision) -> DecisionView:
    return DecisionView(
        occurred_at=decision.occurred_at,
        author=_actor_view(decision.author),
        rationale=decision.rationale,
        outcome=decision.outcome,
    )


def _milestone_view(milestone: Milestone) -> MilestoneView:
    return MilestoneView(
        identifier=milestone.identifier,
        name=milestone.name,
        status=milestone.status,
        completed_at=milestone.completed_at,
    )


def to_engagement_view(engagement: Engagement) -> EngagementView:
    """Create a detached immutable view of an Engagement aggregate."""
    return EngagementView(
        engagement_id=str(engagement.engagement_id),
        owner=_actor_view(engagement.owner),
        goal=_goal_view(engagement.goal),
        status=engagement.status,
        created_at=engagement.created_at,
        updated_at=engagement.updated_at,
        participants=tuple(_participant_view(item) for item in engagement.participants),
        decisions=tuple(_decision_view(item) for item in engagement.decisions),
        milestones=tuple(_milestone_view(item) for item in engagement.milestones),
    )
