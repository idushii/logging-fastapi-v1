from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "authtoken" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "projects" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "device" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uid" VARCHAR(255) NOT NULL UNIQUE,
    "project_id" INT NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "event" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(18) NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL,
    "request_headers" JSONB,
    "request_payload" JSONB,
    "response_headers" JSONB,
    "response_status" INT,
    "response_payload" JSONB,
    "content" JSONB,
    "device_id" INT NOT NULL REFERENCES "device" ("id") ON DELETE CASCADE,
    "project_id" INT NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "event"."type" IS 'START_HTTP_REQUEST: start_http_request\nEND_HTTP_REQUEST: end_http_request\nLOG: log\nCHANGE_APP_STATE: change_app_state\nAPP_START: app_start\nAPP_STOP: app_stop\nCACHE_CHANGE: cache_change';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL,
    "role" VARCHAR(5) NOT NULL  DEFAULT 'user'
);
COMMENT ON COLUMN "users"."role" IS 'USER: user\nADMIN: admin';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "projects_authtoken" (
    "projects_id" INT NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE,
    "authtoken_id" INT NOT NULL REFERENCES "authtoken" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users_projects" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "project_id" INT NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
