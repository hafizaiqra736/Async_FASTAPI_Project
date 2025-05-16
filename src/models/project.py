# src/models/project.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from src.config.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    place = Column(String, nullable=True)
    start_date = Column(Date)
    estimated_end_date = Column(Date)
    description = Column(String, nullable=True) 
    budget = Column(Float, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
    

    tasks = relationship("Task", back_populates="project", lazy="selectin")

