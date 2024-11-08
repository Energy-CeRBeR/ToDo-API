from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.categories.schemas import CategoryResponse, CategoryCreate, CategoryEdit, SuccessfulResponse
from src.categories.services import CategoryService
from src.categories.exceptions import NotFoundException

from src.users.models import User
from src.users.services import UserService
from src.users.exceptions import AccessException

router = APIRouter(tags=["categories"], prefix="/categories")


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> List[CategoryResponse]:
    categories = await CategoryService().get_all_user_categories(current_user.id)
    return list(map(lambda x: CategoryResponse(**x.to_dict()), categories))


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        category_id: int
) -> CategoryResponse:
    category = await CategoryService().get_category_by_id(category_id)
    if category is None:
        raise NotFoundException()

    return CategoryResponse(**category.to_dict())


@router.post("/", response_model=CategoryResponse)
async def create_category(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        new_category: CategoryCreate
) -> CategoryResponse:
    category = await CategoryService().create_category(new_category, current_user.id)
    return CategoryResponse(**category.to_dict())


@router.put("/{category_id}", response_model=CategoryResponse)
async def edit_category(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        category_id: int,
        edited_category: CategoryEdit
) -> CategoryResponse:
    category = await CategoryService().get_category_by_id(category_id)
    if category is None:
        raise NotFoundException()

    if category.user_id != current_user.id:
        raise AccessException()

    upd_category = await CategoryService().edit_category(category, edited_category)

    return CategoryResponse(**upd_category.to_dict())


@router.delete("/{category_id}", response_model=SuccessfulResponse)
async def delete_category(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        category_id: int
) -> SuccessfulResponse:
    category = await CategoryService().get_category_by_id(category_id)

    if category is None:
        raise NotFoundException()
    if category.user_id != current_user.id:
        raise AccessException()

    await CategoryService().delete_category(category)

    return SuccessfulResponse()
