from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import List
from pydantic import BaseModel
from auth import get_current_user
from models import Event as EventBase, EventType, User
from tortoise.contrib.pydantic import pydantic_model_creator

from websocket import WebSocketManager

router = APIRouter(tags=["Events"])

class EventCreate(BaseModel):
    event_type: EventType
    payload: str
    device_id: int

class EventUpdate(BaseModel):
    event_type: EventType
    payload: str

Event = pydantic_model_creator(EventBase)

@router.get("/events/", response_model=List[Event])
async def list_events(current_user: User = Depends(get_current_user)):
    events = await EventBase.all()
    return events

@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: int, current_user: User = Depends(get_current_user)):
    event = await EventBase.get(id=event_id)
    return event

@router.post("/events/", response_model=Event)
async def create_event(event: EventCreate, current_user: User = Depends(get_current_user)):
    new_event = await EventBase.create(**event.dict())
    return new_event

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: EventUpdate, current_user: User = Depends(get_current_user)):
    updated_event = await EventBase.filter(id=event_id).update(**event.dict())
    return updated_event

@router.delete("/events/{event_id}", response_model=Event)
async def delete_event(event_id: int, current_user: User = Depends(get_current_user)):
    event = await EventBase.get(id=event_id)
    await EventBase.delete()
    return event

@router.websocket("/ws/{device_uid}/{project_id}")
async def websocket_endpoint(websocket: WebSocket, device_uid: str, project_id: str):
    await WebSocketManager.connect(websocket, device_uid, project_id)
    try:
        while True:
            data = await websocket.receive_text()
            await WebSocketManager.process_message(data, device_uid, project_id)
    except WebSocketDisconnect:
        WebSocketManager.disconnect(device_uid)
