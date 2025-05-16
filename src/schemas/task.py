# src/schemas/task.py

from pydantic import BaseModel
from typing import Optional, List
from src.schemas.comment import CommentResponse


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    project_id: int
    comments: List[CommentResponse] = []

    model_config = {
        "from_attributes": True
    }
