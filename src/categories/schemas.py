from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.tasks.schemas import TaskResponse

from src.categories.models import Colors


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class CategoryCreate(BaseModel):
    name: str
    color: Colors


class CategoryEdit(BaseModel):
    name: str
    color: Colors


class CategoryResponse(BaseModel):
    id: int
    name: str
    color: Colors
    user_id: int
    created_at: datetime
    tasks: List[TaskResponse]
