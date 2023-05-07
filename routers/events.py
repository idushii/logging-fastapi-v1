from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from models import Event as EventBase, EventType
from tortoise.contrib.pydantic import pydantic_model_creator

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
async def list_events():
    events = await Event.all()
    return events

@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: int):
    event = await Event.get(id=event_id)
    return event

@router.post("/events/", response_model=Event)
async def create_event(event: EventCreate):
    new_event = await Event.create(**event.dict())
    return new_event

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: EventUpdate):
    updated_event = await Event.filter(id=event_id).update(**event.dict())
    return updated_event

@router.delete("/events/{event_id}", response_model=Event)
async def delete_event(event_id: int):
    event = await Event.get(id=event_id)
    await event.delete()
    return event
