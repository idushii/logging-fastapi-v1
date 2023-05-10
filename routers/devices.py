from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from auth import get_current_user
from models import Device as DeviceBase, User
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(tags=["Deveices"])

class DeviceCreate(BaseModel):
    description: str
    project_id: int

class DeviceUpdate(BaseModel):
    description: str

Device = pydantic_model_creator(DeviceBase)

# Роут для получния списка девайсов
@router.get("/devices/", response_model=List[Device])
async def list_devices(current_user: User = Depends(get_current_user)):
    devices = await DeviceBase.all()
    return devices

# Роут для получния конкретного девайса
@router.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: int, current_user: User = Depends(get_current_user)):
    device = await DeviceBase.get(id=device_id)
    return device

# Роут для создания нового девайса
@router.post("/devices/", response_model=Device)
async def create_device(device: DeviceCreate, current_user: User = Depends(get_current_user)):
    new_device = await DeviceBase.create(**device.dict())
    return new_device

# Роут для обновления девайса
@router.put("/devices/{device_id}", response_model=Device)
async def update_device(device_id: int, device: DeviceUpdate, current_user: User = Depends(get_current_user)):
    updated_device = await DeviceBase.filter(id=device_id).update(**device.dict())
    return updated_device

# Роут для удаления девайса
@router.delete("/devices/{device_id}", response_model=Device)
async def delete_device(device_id: int, current_user: User = Depends(get_current_user)):
    device = await DeviceBase.get(id=device_id)
    await DeviceBase.delete()
    return device
