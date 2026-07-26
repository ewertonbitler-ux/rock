"""Application-layer failures for Engagement use cases."""

from __future__ import annotations


class EngagementApplicationError(Exception):
    """Base class for Engagement application orchestration failures."""


class EngagementNotFound(EngagementApplicationError):
    """Raised when an Engagement cannot be loaded by its canonical identity."""


class EngagementAlreadyExists(EngagementApplicationError):
    """Raised when creating an Engagement with an identity already in use."""
