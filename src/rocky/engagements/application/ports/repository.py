"""Repository port owned by the Engagement application boundary."""

from __future__ import annotations

from typing import Protocol

from rocky.engagements.domain import Engagement, EngagementId


class EngagementRepository(Protocol):
    """Minimal persistence-neutral contract for Engagement aggregates."""

    def get(self, engagement_id: EngagementId) -> Engagement | None:
        """Return an Engagement or ``None`` when the identity is absent."""
        ...

    def add(self, engagement: Engagement) -> None:
        """Persist a newly created Engagement aggregate."""
        ...

    def save(self, engagement: Engagement) -> None:
        """Persist changes to an existing Engagement aggregate."""
        ...
