import datetime
from pydantic import BaseModel

from src.tasks.models import Priority


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class TaskCreate(BaseModel):
    name: str
    description: str
    priority: Priority
    category_id: int
    date: datetime.date


class TaskEdit(BaseModel):
    name: str
    description: str
    category_id: int
    date: datetime.date


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    completed: bool
    user_id: int
    category_id: int
    date: datetime.date
