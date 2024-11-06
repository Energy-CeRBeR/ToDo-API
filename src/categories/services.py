from typing import List

from src.categories.models import Category
from src.categories.repositories import CategoryRepository
from src.categories.schemas import CategoryCreate, CategoryEdit


class CategoryService:
    repository = CategoryRepository()

    async def create_category(self, category: CategoryCreate, user_id: int) -> Category:
        return await self.repository.create_category(category, user_id)

    async def edit_category(self, category: Category, category_edit: CategoryEdit) -> Category:
        return await self.repository.edit_category(category, category_edit)

    async def get_category_by_id(self, category_id: int) -> Category:
        return await self.repository.get_category_by_id(category_id)

    async def get_all_user_categories(self, user_id: int) -> List[Category]:
        return await self.repository.get_all_user_categories(user_id)

    async def delete_category(self, category: Category) -> None:
        return await self.repository.delete_category(category)
