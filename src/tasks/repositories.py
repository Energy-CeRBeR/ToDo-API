import random
from typing import Optional

from sqlalchemy import insert, select, delete, update

from src.tasks.models import Task
from src.tasks.schemas import TaskCreate, TaskEdit

from src.database import async_session


class TaskRepository:

    async def generate_id(self) -> int:
        unique_id = random.randint(10000000, 99999999)
        while await self.get_task_by_id(unique_id):
            unique_id = random.randint(10000000, 99999999)

        return unique_id

    async def create_task(self, task: TaskCreate, user_id: int) -> Task:
        task_dc = task.dict()
        task_dc["user_id"] = user_id
        task_dc["id"] = await self.generate_id()
        async with async_session() as session:
            stmt = insert(Task).values(**task_dc)
            await session.execute(stmt)
            await session.commit()

            new_task: Task = await self.get_task_by_id(task_dc["id"])
            return new_task

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        async with async_session() as session:
            stmt = select(Task).where(Task.id == task_id)
            result = await session.execute(stmt)
            task = result.scalars().first()

            return task

    async def edit_task(self, task: Task, edited_task: TaskEdit) -> Task:
        task_dc = edited_task.dict()
        task_dc["priority"] = task.priority
        async with async_session() as session:
            stmt = update(Task).where(Task.id == task.id).values(**task_dc)
            await session.execute(stmt)
            await session.commit()

            task: Task = await self.get_task_by_id(task.id)
            return task

    async def edit_task_status(self, task: Task) -> Task:
        async with async_session() as session:
            stmt = update(Task).where(Task.id == task.id).values(completed=False if task.completed else True)
            await session.execute(stmt)
            await session.commit()

            task: Task = await self.get_task_by_id(task.id)
            return task

    async def delete_task(self, task: Task) -> None:
        async with async_session() as session:
            stmt = delete(Task).where(Task.id == task.id)
            await session.execute(stmt)
            await session.commit()
