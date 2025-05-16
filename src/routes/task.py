# src/routes/task.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from src.models.task import Task
from src.models.project import Project
from src.schemas.task import TaskCreate, TaskResponse
from src.config.database import get_db
from src.utils.token import get_current_user
from src.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/{project_id}", response_model=TaskResponse)
async def create_task(
    project_id: int,
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check ownership of project
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=project_id,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/{project_id}", response_model=List[TaskResponse])
async def get_project_tasks(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify user owns the project
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Eagerly load comments to avoid MissingGreenlet error if TaskResponse includes them
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.comments))
        .where(Task.project_id == project_id)
    )
    return result.scalars().all()


@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Query the task with its comments in a proper async context
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.comments))
        .where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify if the task belongs to the current user's project
    project_check = await db.execute(
        select(Project).where(Project.id == task.project_id, Project.owner_id == current_user.id)
    )
    if not project_check.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return TaskResponse.from_orm(task)

