"""Public Engagement domain errors."""

from __future__ import annotations


class EngagementError(Exception):
    """Base error for the Engagement domain."""


class InvalidEngagementId(EngagementError):
    pass


class InvalidActor(EngagementError):
    pass


class InvalidGoal(EngagementError):
    pass


class InvalidLifecycleTransition(EngagementError):
    pass


class DuplicateParticipant(EngagementError):
    pass


class ParticipantNotFound(EngagementError):
    pass


class OwnerCannotBeParticipant(EngagementError):
    pass


class InvalidDecision(EngagementError):
    pass


class InvalidMilestone(EngagementError):
    pass


class DuplicateMilestone(EngagementError):
    pass


class MilestoneNotFound(EngagementError):
    pass


class CompletedMilestoneImmutable(EngagementError):
    pass
