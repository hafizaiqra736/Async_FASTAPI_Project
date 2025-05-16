# src/main.py
from fastapi import FastAPI
from src.routes import auth, project, task, comment

app = FastAPI()

app.include_router(auth.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(comment.router)
from src.routes import project
print("Imported project module =", project)
print("Has router? ", hasattr(project, "router"))
