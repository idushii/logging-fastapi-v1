import datetime
from tortoise import fields
from tortoise.models import Model
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class EventType(str, Enum):
    START_HTTP_REQUEST = "start_http_request"
    END_HTTP_REQUEST = "end_http_request"
    LOG = "log"
    CHANGE_APP_STATE = "change_app_state"
    APP_START = "app_start"
    APP_STOP = "app_stop"
    CACHE_CHANGE = "cache_change"

class AuthToken(Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.token
    
class Project(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    tokens = fields.ManyToManyField("models.AuthToken", related_name="auth_tokens")

    def __str__(self):
        return self.name

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password_hash = fields.CharField(max_length=128)
    role = fields.CharEnumField(UserRole, default=UserRole.USER)
    projects = fields.ManyToManyField("models.Project", related_name="users")

    def __str__(self):
        return self.username

class Device(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=255)
    project = fields.ForeignKeyField("models.Project", related_name="devices")

    def __str__(self):
        return self.description


class Event(Model):
    id = fields.IntField(pk=True)
    type = fields.CharEnumField(EventType)
    timestamp = fields.DatetimeField(default=datetime.datetime.utcnow)
    device = fields.ForeignKeyField("models.Device", related_name="events")
    project = fields.ForeignKeyField("models.Project", related_name="events")

    # Для http-запросов
    request_headers = fields.JSONField(null=True)
    request_payload = fields.JSONField(null=True)
    response_headers = fields.JSONField(null=True)
    response_status = fields.IntField(null=True)
    response_payload = fields.JSONField(null=True)

    # Для логов и изменения состояния приложения
    content = fields.JSONField(null=True)

    def __str__(self):
        return f"{self.type} at {self.timestamp}"
