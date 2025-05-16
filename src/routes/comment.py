#src/routes/comment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.models.comment import Comment
from src.models.task import Task
from src.models.project import Project
from src.schemas.comment import CommentCreate, CommentResponse
from src.config.database import get_db
from src.utils.token import get_current_user
from src.models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/{task_id}", response_model=CommentResponse)
async def create_comment(
    task_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if task exists and user owns the project
    task_result = await db.execute(select(Task).where(Task.id == task_id))
    task = task_result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project_check = await db.execute(
        select(Project).where(Project.id == task.project_id, Project.owner_id == current_user.id)
    )
    if not project_check.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Unauthorized to comment on this task")

    new_comment = Comment(content=comment.content, task_id=task_id, user_id=current_user.id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


@router.get("/{task_id}", response_model=List[CommentResponse])
async def get_comments_for_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check task ownership via project
    task_result = await db.execute(select(Task).where(Task.id == task_id))
    task = task_result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project_check = await db.execute(
        select(Project).where(Project.id == task.project_id, Project.owner_id == current_user.id)
    )
    if not project_check.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not authorized to view comments")

    result = await db.execute(select(Comment).where(Comment.task_id == task_id))
    return result.scalars().all()
