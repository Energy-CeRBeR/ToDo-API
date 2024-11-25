from typing import List

from src.tasks.models import Task
from src.tasks.repositories import TaskRepository
from src.tasks.schemas import TaskCreate, TaskEdit

from src.users.exceptions import AccessException
from src.tasks.exceptions import NotFoundException as TaskNotFoundException

from src.categories.services import CategoryService


class TaskService:
    repository = TaskRepository()

    async def create_task(self, task_create: TaskCreate, user_id: int) -> Task:
        category = await CategoryService().get_category_by_id(task_create.category_id)
        if category.user_id != user_id:
            raise AccessException()

        return await self.repository.create_task(task_create, user_id)

    async def edit_task(self, task_edit: TaskEdit, task_id: int, user_id: int) -> Task:
        category = await CategoryService().get_category_by_id(task_edit.category_id)
        if category.user_id != user_id:
            raise AccessException()

        task = await self.get_task_by_id(task_id, user_id)
        if task.user_id != user_id:
            raise AccessException()

        return await self.repository.edit_task(task, task_edit)

    async def get_task_by_id(self, task_id: int, user_id: int) -> Task:
        task = await self.repository.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundException()
        if task.user_id != user_id:
            raise AccessException()

        return task

    async def get_all_user_tasks(self, user_id: int) -> List[Task]:
        return await self.repository.get_all_user_tasks(user_id)

    async def change_task_status(self, task_id: int, user_id: int) -> Task:
        task = await self.get_task_by_id(task_id)
        if task.user_id != user_id:
            raise AccessException()

        return await self.repository.change_task_status(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.get_task_by_id(task_id, user_id)
        if task.user_id != user_id:
            raise AccessException()

        return await self.repository.delete_task(task)

    async def uncompleted_all_user_tasks(self, user_id: int) -> None:
        await self.repository.uncompleted_all_user_tasks(user_id)

    async def uncompleted_all_tasks(self) -> None:
        await self.repository.uncompleted_all_tasks()

    async def delete_all_user_tasks(self, user_id: int) -> None:
        await self.repository.delete_all_user_tasks(user_id)

    async def delete_all_tasks(self) -> None:
        await self.repository.delete_all_tasks()
