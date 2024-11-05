from datetime import datetime
from pydantic import BaseModel

from src.tasks.models import Priority


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class TaskCreate(BaseModel):
    name: str
    description: str
    priority: Priority
    completed: bool
    category_id: int
    created_at: datetime


class TaskEdit(BaseModel):
    name: str
    description: str
    completed: bool
    category_id: int
    created_at: datetime


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    completed: bool
    user_id: int
    category_id: int
    created_at: datetime
