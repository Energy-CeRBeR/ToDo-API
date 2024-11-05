from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from src.tasks.schemas import TaskResponse, TaskCreate, TaskEdit, SuccessfulResponse
from src.tasks.services import TaskService

from src.users.models import User
from src.users.services import UserService

router = APIRouter(tags=["tasks"], prefix="/tasks")


@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks(current_user: Annotated[User, Depends(UserService().get_current_user)]) -> List[TaskResponse]:
    tasks = await TaskService().get_all_user_tasks(current_user.id)
    return list(map(lambda x: TaskResponse(**x.to_dict()), tasks))


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        task_id: int
) -> TaskResponse:
    task = await TaskService().get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(**task.to_dict())


@router.post("/", response_model=TaskResponse)
async def create_task(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        new_task: TaskCreate
) -> TaskResponse:
    task = await TaskService().create_task(new_task, current_user.id)
    return TaskResponse(**task.to_dict())


@router.put("/{task_id}", response_model=TaskResponse)
async def edit_task(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        task_id: int,
        edited_task: TaskEdit
) -> TaskResponse:
    task = await TaskService().get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied!")

    upd_task = await TaskService().edit_task(task, edited_task)

    return TaskResponse(**upd_task.to_dict())


@router.put("/{task_id}/change_status", response_model=TaskResponse)
async def change_task_status(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        task_id: int
) -> TaskResponse:
    task = await TaskService().get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied!")

    upd_task = await TaskService().change_task_status(task)

    return TaskResponse(**upd_task.to_dict())


@router.delete("/{task_id}", response_model=SuccessfulResponse)
async def delete_task(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        task_id: int
) -> SuccessfulResponse:
    task = await TaskService().get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied!")

    await TaskService().delete_task(task)

    return SuccessfulResponse()
