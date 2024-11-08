import random
from typing import Optional, List

from sqlalchemy import insert, select, delete, update

from config_data.config import Config, load_config
from utils import auth_settings
from src.database import async_session

from src.users.models import User
from src.users.schemas import UserCreate, UserEdit
from src.users.exceptions import EmailExistsException, ShortNameExistsException


class AdminRepository:
    async def get_all_users(self) -> List[User]:
        async with async_session() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()

            return users

    async def delete_user_by_id(self, user_id: int) -> None:
        async with async_session() as session:
            stmt = delete(User).where(User.id == user_id)
            await session.execute(stmt)
            await session.commit()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()

        return user

    async def change_admin_status(self, user: User) -> User:
        async with async_session() as session:
            stmt = update(User).where(User.id == user.id).values(is_admin=False if user.is_admin else True)
            await session.execute(stmt)
            await session.commit()

            user: User = await self.get_user_by_id(user.id)
            return user

    async def change_verified_status(self, user: User) -> User:
        async with async_session() as session:
            stmt = update(User).where(User.id == user.id).values(is_verified=False if user.is_verified else True)
            await session.execute(stmt)
            await session.commit()

            user: User = await self.get_user_by_id(user.id)
            return user

    async def change_active_status(self, user: User) -> User:
        async with async_session() as session:
            stmt = update(User).where(User.id == user.id).values(is_active=False if user.is_active else True)
            await session.execute(stmt)
            await session.commit()

            user: User = await self.get_user_by_id(user.id)
            return user
