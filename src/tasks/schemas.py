import datetime
from typing import Annotated
from pydantic import BaseModel, Field

from src.tasks.models import Priority


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class TaskCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(max_length=100)]
    priority: Priority
    category_id: int
    date: datetime.date


class TaskEdit(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(max_length=100)]
    priority: Priority
    category_id: int
    date: datetime.date


class TaskResponse(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(max_length=100)]
    priority: Priority
    completed: bool
    category_id: int
    date: datetime.date
