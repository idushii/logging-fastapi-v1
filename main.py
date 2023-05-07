from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres@localhost:5432/logging_fastapi"},
    "apps": {
        "models": {
            "models": ["main", "aerich.models"],
            "default_connection": "default",
        }
    },
}

register_tortoise(
    app,
    db_url="postgres://postgres@localhost:5432/logging_fastapi",
    modules={"models": ["main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
