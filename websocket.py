import json
from typing import Dict
from fastapi import WebSocket
from models import Device, Event, EventType
import datetime


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, device_uid: str, project_id: str):
        device, created = await Device.get_or_create(uid=device_uid, project_id=project_id)
        await websocket.accept()
        self.active_connections[device.id] = websocket

    async def process_message(self, message: str, device_uid: str, project_id: str):
        data = json.loads(message)
        event_type = data["type"]
        device = await Device.get(uid=device_uid, project_id=project_id)

        event = Event(type=event_type, device=device, project_id=project_id)

        if event_type == EventType.START_HTTP_REQUEST or event_type == EventType.END_HTTP_REQUEST:
            event.request_headers = data["request_headers"]
            event.request_payload = data["request_payload"]
            event.response_headers = data.get("response_headers")
            event.response_status = data.get("response_status")
            event.response_payload = data.get("response_payload")
        elif event_type in [EventType.LOG, EventType.APP_START, EventType.APP_STOP, EventType.CACHE_CHANGE, EventType.CHANGE_APP_STATE]:
            event.content = data["content"]

        await event.save()

    async def disconnect(self, device_uid: str):
        device = await Device.get(uid=device_uid)
        if device and device.id in self.active_connections:
            del self.active_connections[device.id]
