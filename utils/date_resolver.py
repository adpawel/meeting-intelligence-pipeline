"""
Deterministic deadline resolver.

Converts structured semantic deadline representations into ISO timestamps.
"""

from datetime import datetime, timedelta
from models import Deadline


def compute_deadline(deadline: Deadline, base: datetime) -> str | None:
    """
    Convert a structured Deadline object into ISO 8601 timestamp.

    Args:
        deadline (Deadline): Structured deadline object.
        base (datetime): Reference datetime (usually meeting date).

    Returns:
        str | None: ISO formatted datetime string or None if not computable.
    """

    if deadline.type == "none":
        return None

    if deadline.type == "relative_days":
        target = base + timedelta(days=deadline.days or 0)
        return target.isoformat()

    if deadline.type == "weekday":
        current_weekday = base.weekday()
        days_ahead = (deadline.weekday - current_weekday) % 7
        days_ahead = days_ahead if days_ahead != 0 else 7

        target = base + timedelta(days=days_ahead)

        return target.replace(
            hour=deadline.hour or 0,
            minute=deadline.minute or 0,
            second=0,
            microsecond=0,
        ).isoformat()

    if deadline.type == "calendar_date":
        year = deadline.year or base.year

        target = datetime(
            year,
            deadline.month or 1,
            deadline.day or 1,
            deadline.hour or 0,
            deadline.minute or 0,
        )

        return target.isoformat()

    return None