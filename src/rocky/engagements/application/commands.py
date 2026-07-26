"""Immutable commands for Engagement application use cases."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateEngagement:
    engagement_id: str
    owner_identifier: str
    owner_display_name: str
    goal_title: str
    goal_description: str


@dataclass(frozen=True, slots=True)
class AssignOwner:
    engagement_id: str
    owner_identifier: str
    owner_display_name: str


@dataclass(frozen=True, slots=True)
class AddParticipant:
    engagement_id: str
    actor_identifier: str
    actor_display_name: str
    role: str


@dataclass(frozen=True, slots=True)
class RemoveParticipant:
    engagement_id: str
    actor_identifier: str


@dataclass(frozen=True, slots=True)
class RecordDecision:
    engagement_id: str
    author_identifier: str
    author_display_name: str
    rationale: str
    outcome: str


@dataclass(frozen=True, slots=True)
class RegisterMilestone:
    engagement_id: str
    milestone_identifier: str
    milestone_name: str


@dataclass(frozen=True, slots=True)
class CompleteMilestone:
    engagement_id: str
    milestone_identifier: str


@dataclass(frozen=True, slots=True)
class StartEngagement:
    engagement_id: str


@dataclass(frozen=True, slots=True)
class SuspendEngagement:
    engagement_id: str


@dataclass(frozen=True, slots=True)
class ResumeEngagement:
    engagement_id: str


@dataclass(frozen=True, slots=True)
class CompleteEngagement:
    engagement_id: str


@dataclass(frozen=True, slots=True)
class CancelEngagement:
    engagement_id: str
