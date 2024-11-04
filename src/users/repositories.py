import random
from typing import Optional

from sqlalchemy import insert, select, delete, update

from utils import auth_settings
from src.users.models import User
from src.users.schemas import UserCreate, UserEdit

from fastapi import HTTPException

from src.database import async_session


class UserRepository:
    async def generate_id(self) -> int:
        new_id = random.randint(10000000, 99999999)
        while await self.get_user_by_id(new_id):
            new_id = random.randint(10000000, 99999999)
        return new_id

    async def create_user(self, user: UserCreate) -> User:
        async with async_session() as session:
            query = select(User).where(User.email == user.email)
            result = await session.execute(query)
            potential_user_1 = result.mappings().all()
        if potential_user_1:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        async with async_session() as session:
            query = select(User).where(User.short_name == user.short_name)
            result = await session.execute(query)
            potential_user_2 = result.mappings().all()
        if potential_user_2:
            raise HTTPException(
                status_code=400, detail="User with this shortname already exists"
            )

        password = user.password
        user_dc = user.dict(exclude={"password"})
        user_dc["password_hash"] = auth_settings.hash_password(password)
        user_dc["id"] = await self.generate_id()

        async with async_session() as session:
            stmt = insert(User).values(**user_dc)
            await session.execute(stmt)
            await session.commit()

            query = select(User).where(User.id == user_dc["id"])
            result = await session.execute(query)
            user = result.scalars().first()

        return user

    async def edit_password(self, user: User, password: str) -> None:
        async with async_session() as session:
            new_hashed_password = auth_settings.hash_password(password)
            stmt = update(User).where(User.id == user.id).values(password_hash=new_hashed_password)
            await session.execute(stmt)
            await session.commit()

    async def edit_info(self, user: User, user_edit: UserEdit) -> User:
        async with async_session() as session:
            stmt = update(User).where(User.id == user.id).values(**user_edit.dict())
            await session.execute(stmt)
            await session.commit()

        upd_user = await self.get_user_by_id(user.id)
        return upd_user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
        return user

    async def get_user_by_short_name(self, short_name: str) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.short_name == short_name)
            result = await session.execute(query)
            user = result.scalars().first()
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()

        return user

    async def delete_user(self, user: User) -> None:
        async with async_session() as session:
            stmt = delete(User).where(User.id == user.id)
            await session.execute(stmt)
            await session.commit()
