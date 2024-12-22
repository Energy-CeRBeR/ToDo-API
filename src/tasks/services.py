from typing import List

from src.categories.exceptions import NotFoundException as CategoryNotFoundException
from src.categories.models import Category
from src.tasks.models import Task
from src.tasks.repositories import TaskRepository
from src.tasks.schemas import TaskCreate, TaskEdit
from src.tasks.exceptions import NotFoundException as TaskNotFoundException

from src.categories.services import CategoryService
from src.users.models import User


class TaskService:
    repository = TaskRepository()

    async def create_task(self, task_create: TaskCreate, user: User) -> Task:
        await CategoryService().get_category_by_id(task_create.category_id, user)
        return await self.repository.create_task(task_create, user.id)

    async def edit_task(self, task_edit: TaskEdit, task_id: int, user: User) -> Task:
        await CategoryService().get_category_by_id(task_edit.category_id, user)
        return await self.repository.edit_task(await self.get_task_by_id(task_id, user.id), task_edit)

    async def get_task_by_id(self, task_id: int, user_id: int) -> Task:
        task = await self.repository.get_task_by_id(task_id)
        if task is None or task.user_id != user_id:
            raise TaskNotFoundException()

        return task

    async def get_all_user_tasks(self, user_id: int) -> List[Task]:
        return await self.repository.get_all_user_tasks(user_id)

    async def get_all_tasks_from_category(self, category: Category, user: User) -> List[Task]:
        if category is None or category.user_id != user.id:
            raise CategoryNotFoundException()

        return await self.repository.get_all_tasks_from_category(category.id)

    async def set_base_category_for_task(self, task: Task, user: User):
        if task.user_id != user.id:
            raise TaskNotFoundException()

        return await self.repository.set_base_category_for_task(task, user.base_category_id)

    async def change_task_status(self, task_id: int, user_id: int) -> Task:
        return await self.repository.change_task_status(await self.get_task_by_id(task_id, user_id))

    async def delete_task(self, task_id: int, user_id: int) -> None:
        return await self.repository.delete_task(await self.get_task_by_id(task_id, user_id))

    async def uncompleted_all_user_tasks(self, user_id: int) -> None:
        await self.repository.uncompleted_all_user_tasks(user_id)

    async def uncompleted_all_tasks(self) -> None:
        await self.repository.uncompleted_all_tasks()

    async def delete_all_user_tasks(self, user_id: int) -> None:
        await self.repository.delete_all_user_tasks(user_id)

    async def delete_all_tasks(self) -> None:
        await self.repository.delete_all_tasks()
