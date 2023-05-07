from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from models import User as UserBase, UserRole
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(tags=["Users"])

User = pydantic_model_creator(UserBase)

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    username: str
    password: str
    role: UserRole

@router.get("/users/", response_model=List[User])
async def list_users():
    users = await User.all()
    return users


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await UserBase.get(id=user_id)
    return user

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    new_user = await UserBase.create(**user.dict())
    return new_user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    updated_user = await UserBase.filter(id=user_id).update(**user.dict())
    return updated_user

@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    user = await UserBase.get(id=user_id)
    await user.delete()
    return user
