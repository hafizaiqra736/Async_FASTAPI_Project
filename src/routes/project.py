#src/routes/project.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.orm import selectinload


from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectResponse
from src.config.database import get_db
from src.utils.token import get_current_user
from src.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    new_project = Project(
        name=project.name,
        place=project.place,
        start_date=project.start_date,
        estimated_end_date=project.estimated_end_date,
        description=project.description,
        budget=project.budget,
        owner_id=project.owner_id,  # Assuming owner_id is part of the ProjectCreate schema
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    # ✅ Use `selectinload` to load tasks eagerly
    stmt = select(Project).options(selectinload(Project.tasks)).where(Project.id == new_project.id)
    result = await db.execute(stmt)
    project_with_tasks = result.scalars().first()

    if not project_with_tasks:
        raise HTTPException(status_code=404, detail="Project not found after creation")

    return project_with_tasks



@router.get("/", response_model=List[ProjectResponse])
async def get_user_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Project).where(Project.owner_id == current_user.id))
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_by_id(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
    select(Project).options(selectinload(Project.tasks)).where(Project.id == project_id)
)

    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

print("Loaded project.py, router =", router)

