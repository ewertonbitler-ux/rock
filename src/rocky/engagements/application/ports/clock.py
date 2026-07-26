"""Time port owned by the Engagement application boundary."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol


class Clock(Protocol):
    """Provide the current timezone-aware instant."""

    def __call__(self) -> datetime:
        """Return the current timezone-aware instant."""
        ...


class SystemClock:
    """Production clock backed by the system UTC time."""

    def __call__(self) -> datetime:
        return datetime.now(UTC)
