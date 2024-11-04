from typing import Annotated

from fastapi import APIRouter, Depends

from src.users.models import User
from src.users.schemas import UserCreate, Token, UserResponse, SuccessfulResponse, UserEdit
from src.users.services import UserService

router = APIRouter(tags=["user"], prefix="/user")


@router.post("/register")
async def register(user_create: UserCreate) -> Token:
    user = await UserService().create_user(user_create)
    access_token = UserService().create_access_token(user)
    refresh_token = UserService().create_refresh_token(user)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=Token)
async def authenticate_user_jwt(user: User = Depends(UserService().authenticate_user)) -> Token:
    access_token = UserService().create_access_token(user)
    refresh_token = UserService().create_refresh_token(user)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token, response_model_exclude_none=True)
async def refresh_jwt(
        user: Annotated[User, Depends(UserService().get_current_user_for_refresh)]
) -> Token:
    access_token = UserService().create_access_token(user)
    return Token(access_token=access_token)


@router.post("/edit_password", response_model=SuccessfulResponse)
async def edit_user_password(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        new_password: str
) -> SuccessfulResponse:
    await UserService().edit_user_password(current_user, new_password)
    return SuccessfulResponse()


@router.get("/self", response_model=UserResponse)
async def login_for_access_token(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> UserResponse:
    return UserResponse(**current_user.to_dict())


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int) -> UserResponse:
    user = await UserService().get_user_by_id(user_id)
    return UserResponse(**user.to_dict())


@router.put("/edit", response_model=UserResponse)
async def edit_user(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        user_edit: UserEdit
) -> UserResponse:
    upd_user = await UserService().edit_user_info(current_user, user_edit)
    return UserResponse(**upd_user.to_dict())


@router.delete("", response_model=SuccessfulResponse)
async def delete_user(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> SuccessfulResponse:
    await UserService().delete_user(current_user)
    return SuccessfulResponse()
