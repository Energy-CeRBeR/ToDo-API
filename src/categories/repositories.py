import random
from typing import Optional, List

from sqlalchemy import insert, select, delete, update

from config_data.config import Config, load_config
from src.categories.models import Category
from src.categories.schemas import CategoryCreate, CategoryEdit

from src.database import async_session

settings: Config = load_config(".env")
global_vars = settings.variablesData


class CategoryRepository:

    async def generate_id(self) -> int:
        unique_id = random.randint(global_vars.MIN_ID, global_vars.MAX_ID)
        while await self.get_category_by_id(unique_id):
            unique_id = random.randint(global_vars.MIN_ID, global_vars.MAX_ID)

        return unique_id

    async def create_category(self, category: CategoryCreate, user_id: int) -> Category:
        category_dc = category.dict()
        category_dc["user_id"] = user_id
        category_dc["id"] = await self.generate_id()
        async with async_session() as session:
            stmt = insert(Category).values(**category_dc)
            await session.execute(stmt)
            await session.commit()

            new_category: Category = await self.get_category_by_id(category_dc["id"])
            return new_category

    async def get_category_by_id(self, category_id: int) -> Optional[Category]:
        async with async_session() as session:
            stmt = select(Category).where(Category.id == category_id)
            result = await session.execute(stmt)
            category = result.scalars().first()

            return category

    async def get_all_user_categories(self, user_id: int) -> List[Category]:
        async with async_session() as session:
            stmt = select(Category).where(Category.user_id == user_id)
            result = await session.execute(stmt)
            categories = result.scalars().all()

        return categories

    async def edit_category(self, category: Category, edited_category: CategoryEdit) -> Category:
        category_dc = edited_category.dict()
        async with async_session() as session:
            stmt = update(Category).where(Category.id == category.id).values(**category_dc)
            await session.execute(stmt)
            await session.commit()

            category: Category = await self.get_category_by_id(category.id)
            return category

    async def delete_category(self, category: Category) -> None:
        async with async_session() as session:
            stmt = delete(Category).where(Category.id == category.id)
            await session.execute(stmt)
            await session.commit()
