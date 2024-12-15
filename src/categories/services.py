from typing import List

from src.categories.models import Category
from src.categories.repositories import CategoryRepository
from src.categories.schemas import CategoryCreate, CategoryEdit
from src.categories.exceptions import NotFoundException

from src.users.models import User


class CategoryService:
    repository = CategoryRepository()

    async def create_category(self, category: CategoryCreate, user_id: int) -> Category:
        return await self.repository.create_category(category, user_id)

    async def edit_category(self, category_edit: CategoryEdit, category_id: int, user: User) -> Category:
        category = await self.get_category_by_id(category_id, user)
        if category.id == user.base_category_id:
            raise NotFoundException()

        return await self.repository.edit_category(category, category_edit)

    async def get_category_by_id(self, category_id: int, user: User) -> Category:
        category = await self.repository.get_category_by_id(category_id)
        if category is None or category.user_id != user.id:
            raise NotFoundException()

        return category

    async def get_user_category_by_id(self, category_id: int, user: User) -> Category:
        return await self.get_category_by_id(category_id, user)

    async def get_all_categories_without_base(self, user: User) -> List[Category]:
        return await self.repository.get_all_categories_without_base(user.id, user.base_category_id)

    async def get_all_user_categories(self, user_id: int) -> List[Category]:
        return await self.repository.get_all_user_categories(user_id)

    async def delete_category(self, category_id: int, user: User) -> None:
        category = await self.get_category_by_id(category_id, user)
        if category.id == user.base_category_id:
            raise NotFoundException()

        return await self.repository.delete_category(category)

    async def delete_all_user_categories(self, user_id: int) -> None:
        await self.repository.delete_all_user_categories(user_id)

    async def delete_all_categories(self) -> None:
        await self.repository.delete_all_categories()
