from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.users.models import User
from src.users.schemas import UserResponse, SuccessfulResponse
from src.users.services import UserService

router = APIRouter(tags=["admin"], prefix="/admin")


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
        current_admin: Annotated[User, Depends(UserService().get_current_admin_user)],  # noqa
) -> List[UserResponse]:
    users = await UserService().get_all_users()
    return list(map(lambda x: UserResponse(**x.to_dict()), users))


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
        current_admin: Annotated[User, Depends(UserService().get_current_admin_user)],  # noqa
        user_id: int
) -> UserResponse:
    user = await UserService().get_user_by_id(user_id)
    return UserResponse(**user.to_dict())


@router.put("/users/{user_id}/change_admin_status")
async def change_admin_status(
        current_admin: Annotated[User, Depends(UserService().get_current_admin_user)],  # noqa
        user_id: int
) -> UserResponse:
    user = await UserService().change_admin_status(user_id)
    return UserResponse(**user.to_dict())


@router.put("/users/{user_id}/change_verified_status")
async def change_verified_status(
        current_admin: Annotated[User, Depends(UserService().get_current_admin_user)],  # noqa
        user_id: int
) -> UserResponse:
    user = await UserService().change_verified_status(user_id)
    return UserResponse(**user.to_dict())


@router.put("/users/{user_id}/change_active_status")
async def change_active_status(
        current_admin: Annotated[User, Depends(UserService().get_current_admin_user)],  # noqa
        user_id: int
) -> UserResponse:
    user = await UserService().change_active_status(user_id)
    return UserResponse(**user.to_dict())


@router.delete("/users/{user_id}", response_model=SuccessfulResponse)
async def delete_user(
        current_admin: Annotated[User, Depends(UserService().get_current_admin_user)],  # noqa
        user_id: int
) -> SuccessfulResponse:
    await UserService().delete_user_by_id(user_id)
    return SuccessfulResponse()
