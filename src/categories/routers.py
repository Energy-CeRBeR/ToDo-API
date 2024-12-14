from fastapi import APIRouter, Depends
from typing import Annotated, List

from src.categories.schemas import CategoryResponse, CategoryCreate, CategoryEdit, SuccessfulResponse
from src.categories.services import CategoryService

from src.users.models import User
from src.users.services import UserService

router = APIRouter(tags=["categories"], prefix="/categories")


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> List[CategoryResponse]:
    categories = await CategoryService().get_all_user_categories(current_user.id)
    return list(map(lambda x: CategoryResponse(**x.to_dict()), categories))


@router.get("/no_base", response_model=List[CategoryResponse])
async def get_all_categories_without_base(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> List[CategoryResponse]:
    categories = await CategoryService().get_all_categories_without_base(current_user)
    return list(map(lambda x: CategoryResponse(**x.to_dict()), categories))


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
        current_user: Annotated[User, Depends(UserService().get_current_user)],  # noqa
        category_id: int
) -> CategoryResponse:
    category = await CategoryService().get_user_category_by_id(category_id, current_user)
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
    upd_category = await CategoryService().edit_category(edited_category, category_id, current_user)
    return CategoryResponse(**upd_category.to_dict())


@router.delete("/{category_id}", response_model=SuccessfulResponse)
async def delete_category(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        category_id: int
) -> SuccessfulResponse:
    await CategoryService().delete_category(category_id, current_user)
    return SuccessfulResponse()
