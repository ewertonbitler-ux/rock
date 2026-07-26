from datetime import UTC, datetime

import pytest

from rocky.engagements import (
    Actor,
    Decision,
    Engagement,
    EngagementId,
    EngagementStatus,
    Goal,
    Milestone,
    MilestoneStatus,
    Participant,
)
from rocky.engagements.errors import (
    CompletedMilestoneImmutable,
    DuplicateMilestone,
    DuplicateParticipant,
    InvalidEngagementId,
    InvalidLifecycleTransition,
    OwnerCannotBeParticipant,
)

NOW = datetime(2026, 7, 26, 12, tzinfo=UTC)
OWNER = Actor("owner-1", "Owner One")
GOAL = Goal("Deliver Engagement", "Implement the governed Engagement domain.")


def make_engagement() -> Engagement:
    return Engagement.create(EngagementId("ENG-0001"), OWNER, GOAL, at=NOW)


def test_create_engagement_as_draft() -> None:
    engagement = make_engagement()

    assert engagement.status is EngagementStatus.DRAFT
    assert engagement.owner == OWNER
    assert engagement.created_at == NOW


def test_reject_noncanonical_identifier() -> None:
    with pytest.raises(InvalidEngagementId):
        EngagementId("eng-1")


def test_lifecycle_happy_path() -> None:
    engagement = make_engagement()

    engagement.start(at=NOW)
    engagement.suspend(at=NOW)
    engagement.resume(at=NOW)
    engagement.complete(at=NOW)

    assert engagement.status is EngagementStatus.COMPLETED


def test_terminal_engagement_cannot_restart() -> None:
    engagement = make_engagement()
    engagement.start(at=NOW)
    engagement.complete(at=NOW)

    with pytest.raises(InvalidLifecycleTransition):
        engagement.start(at=NOW)


def test_owner_cannot_be_participant() -> None:
    engagement = make_engagement()

    with pytest.raises(OwnerCannotBeParticipant):
        engagement.add_participant(Participant(OWNER, "Reviewer"), at=NOW)


def test_duplicate_participant_is_rejected() -> None:
    engagement = make_engagement()
    participant = Participant(Actor("person-2", "Person Two"), "Contributor")
    engagement.add_participant(participant, at=NOW)

    with pytest.raises(DuplicateParticipant):
        engagement.add_participant(participant, at=NOW)


def test_decisions_are_exposed_as_immutable_collection() -> None:
    engagement = make_engagement()
    decision = Decision(NOW, OWNER, "Need one aggregate", "Use Engagement as root")

    engagement.record_decision(decision, at=NOW)

    assert engagement.decisions == (decision,)


def test_milestone_completion_is_preserved() -> None:
    engagement = make_engagement()
    milestone = Milestone("specification", "Specification accepted")
    engagement.register_milestone(milestone, at=NOW)
    engagement.complete_milestone("specification", at=NOW)

    assert milestone.status is MilestoneStatus.COMPLETED
    assert milestone.completed_at == NOW
    with pytest.raises(CompletedMilestoneImmutable):
        engagement.complete_milestone("specification", at=NOW)


def test_duplicate_milestone_is_rejected_case_insensitively() -> None:
    engagement = make_engagement()
    engagement.register_milestone(Milestone("SPEC", "First"), at=NOW)

    with pytest.raises(DuplicateMilestone):
        engagement.register_milestone(Milestone("spec", "Second"), at=NOW)
