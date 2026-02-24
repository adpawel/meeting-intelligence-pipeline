from pydantic import BaseModel
from typing import Optional, List

class ActionItem(BaseModel):
    task: str
    assignee: str
    deadline: Optional[str]
    confidence: float
    
class ActionItemsResponse(BaseModel):
    items: List[ActionItem]
    