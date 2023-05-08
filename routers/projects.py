from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from auth import get_current_admin, get_current_user
from models import Project as ProjectBase, User
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(tags=["Projects"])

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    name: str

Project = pydantic_model_creator(ProjectBase)

@router.get("/projects/", response_model=List[Project], summary="List all projects")
async def list_projects(current_user: User = Depends(get_current_user)):
    projects = await ProjectBase.all()
    return projects

@router.get("/projects/{project_id}", response_model=Project, summary="Get a single project")
async def get_project(project_id: int, current_user: User = Depends(get_current_user)):
    project = await ProjectBase.get(id=project_id)
    return project

@router.post("/projects/", response_model=Project, summary="Create a new project")
async def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user)):
    new_project = await ProjectBase.create(**project.dict())
    return new_project

@router.put("/projects/{project_id}", response_model=Project, summary="Update a project")
async def update_project(project_id: int, project: ProjectUpdate, current_user: User = Depends(get_current_user)):
    updated_project = await ProjectBase.filter(id=project_id).update(**project.dict())
    return updated_project

@router.delete("/projects/{project_id}", response_model=Project, summary="Delete a project")
async def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    project = await ProjectBase.get(id=project_id)
    await ProjectBase.delete()
    return project
