from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from models import *
from routers import projects, users, auth_tokens, devices, events
from tortoise_config import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app,
    db_url="postgres://postgres@localhost:5432/logging_fastapi",
    modules={"models": ["main", "aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(users.router, prefix="/api/users")
app.include_router(projects.router, prefix="/api/projects")
app.include_router(devices.router, prefix="/api/devices")
app.include_router(events.router, prefix="/api/events")
app.include_router(auth_tokens.router, prefix="/api/auth_tokens")