TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres@localhost:5432/logging_fastapi"},
    "apps": {
        "models": {
            "models": ["main", "aerich.models"],
            "default_connection": "default",
        }
    },
}
