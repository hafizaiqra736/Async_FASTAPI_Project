# src/schemas/project.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from src.schemas.task import TaskResponse  # no change

class ProjectBase(BaseModel):
    name: str
    place: Optional[str] = None
    start_date: Optional[date]
    estimated_end_date: Optional[date]
    description: str  
    budget: float

class ProjectCreate(ProjectBase):
    owner_id: int 

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    tasks: List[TaskResponse] = []

    
    model_config = {
        "from_attributes": True 
    }
