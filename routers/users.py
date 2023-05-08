from datetime import timedelta
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from auth import *
from models import User as UserBase, UserRole
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Users"])

User = pydantic_model_creator(UserBase, exclude = ["password_hash"])

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    username: str
    password: str
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/", response_model=List[User])
async def list_users(current_user: User = Depends(get_current_admin)):
    users = await UserBase.all()
    return users


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, current_user: User = Depends(get_current_admin)):
    user = await UserBase.get(id=user_id)
    return user

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, current_user: User = Depends(get_current_admin)):
    new_user = await UserBase.create(**user.dict())
    return new_user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, current_user: User = Depends(get_current_admin)):
    updated_user = await UserBase.filter(id=user_id).update(**user.dict())
    return updated_user

@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int, current_user: User = Depends(get_current_admin)):
    user = await UserBase.get(id=user_id)
    await user.delete()
    return user
