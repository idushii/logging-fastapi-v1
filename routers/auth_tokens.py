from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from models import AuthToken as AuthTokenBase
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(tags=["AuthToken"])

class AuthTokenCreate(BaseModel):
    token: str
    project_id: int

class AuthTokenUpdate(BaseModel):
    token: str

AuthToken = pydantic_model_creator(AuthTokenBase)

@router.get("/auth_tokens/", response_model=List[AuthToken])
async def list_auth_tokens():
    auth_tokens = await AuthToken.all()
    return auth_tokens

@router.get("/auth_tokens/{auth_token_id}", response_model=AuthToken)
async def get_auth_token(auth_token_id: int):
    auth_token = await AuthToken.get(id=auth_token_id)
    return auth_token

@router.post("/auth_tokens/", response_model=AuthToken)
async def create_auth_token(auth_token: AuthTokenCreate):
    new_auth_token = await AuthToken.create(**auth_token.dict())
    return new_auth_token

@router.put("/auth_tokens/{auth_token_id}", response_model=AuthToken)
async def update_auth_token(auth_token_id: int, auth_token: AuthTokenUpdate):
    updated_auth_token = await AuthToken.filter(id=auth_token_id).update(**auth_token.dict())
    return updated_auth_token

@router.delete("/auth_tokens/{auth_token_id}", response_model=AuthToken)
async def delete_auth_token(auth_token_id: int):
    auth_token = await AuthToken.get(id=auth_token_id)
    await auth_token.delete()
    return auth_token
