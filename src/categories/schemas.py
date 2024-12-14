from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.tasks.schemas import TaskResponse


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class CategoryCreate(BaseModel):
    name: str
    color: str


class CategoryEdit(BaseModel):
    name: str
    color: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str
    user_id: int
    created_at: datetime
    tasks: List[TaskResponse]
