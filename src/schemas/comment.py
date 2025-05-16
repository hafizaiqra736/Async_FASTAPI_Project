# src/schemas/comment.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    timestamp: datetime
    task_id: int
    user_id: Optional[int]


    model_config = {
        "from_attributes": True
    }
