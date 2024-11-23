from typing import List

from src.categories.models import Category
from src.categories.repositories import CategoryRepository
from src.categories.schemas import CategoryCreate, CategoryEdit

from src.categories.exceptions import NotFoundException
from src.users.exceptions import AccessException


class CategoryService:
    repository = CategoryRepository()

    async def create_category(self, category: CategoryCreate, user_id: int) -> Category:
        return await self.repository.create_category(category, user_id)

    async def edit_category(self, category_edit: CategoryEdit, category_id: int, user_id: int) -> Category:
        category = await self.get_category_by_id(category_id)
        if category.user_id != user_id:
            raise AccessException()

        return await self.repository.edit_category(category, category_edit)

    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.repository.get_category_by_id(category_id)
        if category is None:
            raise NotFoundException()

        return category

    async def get_user_category_by_id(self, category_id: int, user_id: int) -> Category:
        category = await self.repository.get_category_by_id(category_id)
        if category is None:
            raise NotFoundException()

        if category.user_id != user_id:
            raise AccessException()

        return category

    async def get_all_user_categories(self, user_id: int) -> List[Category]:
        return await self.repository.get_all_user_categories(user_id)

    async def delete_category(self, category_id: int, user_id: int) -> None:
        category = await self.get_category_by_id(category_id)
        if category.user_id != user_id:
            raise AccessException()

        return await self.repository.delete_category(category)

    async def delete_all_user_categories(self, user_id: int) -> None:
        await self.repository.delete_all_user_categories(user_id)

    async def delete_all_categories(self) -> None:
        await self.repository.delete_all_categories()
