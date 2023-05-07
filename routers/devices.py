from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from models import Device as DeviceBase
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(tags=["Deveices"])

class DeviceCreate(BaseModel):
    description: str
    project_id: int

class DeviceUpdate(BaseModel):
    description: str

Device = pydantic_model_creator(DeviceBase)

@router.get("/devices/", response_model=List[Device])
async def list_devices():
    devices = await Device.all()
    return devices

@router.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: int):
    device = await Device.get(id=device_id)
    return device

@router.post("/devices/", response_model=Device)
async def create_device(device: DeviceCreate):
    new_device = await Device.create(**device.dict())
    return new_device

@router.put("/devices/{device_id}", response_model=Device)
async def update_device(device_id: int, device: DeviceUpdate):
    updated_device = await Device.filter(id=device_id).update(**device.dict())
    return updated_device

@router.delete("/devices/{device_id}", response_model=Device)
async def delete_device(device_id: int):
    device = await Device.get(id=device_id)
    await device.delete()
    return device
