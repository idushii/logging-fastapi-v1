from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from models import Project as ProjectBase
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(tags=["Projects"])

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    name: str

Project = pydantic_model_creator(ProjectBase)

@router.get("/projects/", response_model=List[Project], summary="List all projects")
async def list_projects():
    projects = await Project.all()
    return projects

@router.get("/projects/{project_id}", response_model=Project, summary="Get a single project")
async def get_project(project_id: int):
    project = await Project.get(id=project_id)
    return project

@router.post("/projects/", response_model=Project, summary="Create a new project")
async def create_project(project: ProjectCreate):
    new_project = await Project.create(**project.dict())
    return new_project

@router.put("/projects/{project_id}", response_model=Project, summary="Update a project")
async def update_project(project_id: int, project: ProjectUpdate):
    updated_project = await Project.filter(id=project_id).update(**project.dict())
    return updated_project

@router.delete("/projects/{project_id}", response_model=Project, summary="Delete a project")
async def delete_project(project_id: int):
    project = await Project.get(id=project_id)
    await project.delete()
    return project
