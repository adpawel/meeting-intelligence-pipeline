"""
Data models for the Meeting Assistant.
Defines the structure for action items and API responses using Pydantic.
"""

from typing import List, Optional
from pydantic import BaseModel

class ActionItem(BaseModel):
    """Represents a single task assigned to a person during a meeting."""
    task: str
    assignee: str
    deadline: Optional[str]
    confidence: float

class ActionItemsResponse(BaseModel):
    """Container for a list of action items extracted from the transcript."""
    items: List[ActionItem]