"""Immutable queries for Engagement application use cases."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetEngagement:
    engagement_id: str
