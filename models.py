"""
Data models for structured meeting analysis.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel


class Deadline(BaseModel):
    """
    Structured semantic representation of a deadline.
    This model avoids natural language parsing in business logic.
    """

    type: Literal[
        "weekday",
        "relative_days",
        "calendar_date",
        "conditional",
        "none",
    ]

    weekday: Optional[int] = None
    days: Optional[int] = None
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    depends_on: Optional[str] = None


class ActionItem(BaseModel):
    """
    Represents a single structured task extracted from the meeting.
    """

    task: str
    assignee: str
    deadline: Deadline
    deadline_iso: Optional[str] = None
    confidence: float


class ActionItemsResponse(BaseModel):
    """
    Container object for extracted action items.
    """

    items: List[ActionItem]