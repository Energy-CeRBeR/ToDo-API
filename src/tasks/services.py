from typing import List

from src.tasks.models import Task
from src.tasks.repositories import TaskRepository
from src.tasks.schemas import TaskCreate, TaskEdit


class ReportService:
    repository = TaskRepository()

    async def create_task(self, task: TaskCreate, user_id: int) -> Task:
        return await self.repository.create_task(task, user_id)

    async def edit_task(self, task: Task, task_edit: TaskEdit) -> Task:
        return await self.repository.edit_task(task, task_edit)

    async def get_task_by_id(self, task_id: int) -> Task:
        return await self.repository.get_task_by_id(task_id)

    async def get_all_user_tasks(self, user_id: int) -> List[Task]:
        return await self.repository.get_all_user_tasks(user_id)

    async def change_task_status(self, task: Task) -> Task:
        return await self.repository.change_task_status(task)

    async def delete_task(self, task: Task) -> None:
        return await self.repository.delete_task(task)
