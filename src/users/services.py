import jwt

from datetime import timedelta
from typing import Optional, List
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config_data.config import Config, load_config
from utils.auth_settings import validate_password, decode_jwt, encode_jwt

from src.users.models import User
from src.users.repositories import UserRepository
from src.users.schemas import UserCreate, TokenData, UserEdit, UserLogin
from src.users.exceptions import CredentialException, TokenTypeException, NotFoundException, AccessException, \
    EmailExistsException, ShortNameExistsException

from src.categories.models import Category

http_bearer = HTTPBearer()

settings: Config = load_config(".env")
auth_config = settings.authJWT

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class UserService:
    repository = UserRepository()

    @staticmethod
    def create_jwt(
            token_type: str,
            token_data: dict,
            expire_minutes: int = auth_config.access_token_expire_minutes,
            expire_timedelta: timedelta | None = None
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        token = encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta
        )
        return token

    def create_access_token(self, user: User) -> str:
        jwt_payload = {
            "sub": user.short_name,
            "short_name": user.short_name,
            "email": user.email,
        }
        return self.create_jwt(
            token_type=ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=auth_config.access_token_expire_minutes
        )

    def create_refresh_token(self, user: User) -> str:
        jwt_payload = {
            "sub": user.short_name
        }
        return self.create_jwt(
            token_type=REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(days=auth_config.refresh_token_expire_days)
        )

    async def authenticate_user(self, auth_data: UserLogin) -> Optional[User]:
        user = await self.repository.get_user_by_email(auth_data.email)
        if not user:
            raise CredentialException()
        if not validate_password(auth_data.password, user.password_hash):
            raise CredentialException()

        return user

    @staticmethod
    async def validate_admin_user(user: User) -> User:
        if not user.is_admin:
            raise AccessException()
        return user

    async def validate_user(self, expected_token_type: str, token: str | bytes) -> User:

        try:
            payload = decode_jwt(token=token)
            token_type = payload.get(TOKEN_TYPE_FIELD)
            if token_type != expected_token_type:
                raise TokenTypeException(token_type, expected_token_type)

            short_name: str = payload.get("sub")
            if short_name is None:
                raise CredentialException()
            token_data = TokenData(short_name=short_name)

        except jwt.DecodeError:
            raise CredentialException()
        except jwt.ExpiredSignatureError:
            raise CredentialException()

        user = await self.repository.get_user_by_short_name(token_data.short_name)
        if user is None:
            raise CredentialException()

        return user

    async def set_base_category_id(self, user: User, category: Category) -> User:
        if category.user_id != user.id:
            raise AccessException()
        return await self.repository.set_base_category_id(user, category.id)

    async def get_current_user_for_refresh(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        return await self.validate_user(expected_token_type=REFRESH_TOKEN_TYPE, token=token.credentials)

    async def get_current_user(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        return await self.validate_user(expected_token_type=ACCESS_TOKEN_TYPE, token=token.credentials)

    async def get_current_admin_user(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        current_user = await self.get_current_user(token)
        return await self.validate_admin_user(current_user)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repository.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        return user

    async def get_all_users(self) -> List[User]:
        return await self.repository.get_all_users()

    async def create_user(self, user: UserCreate) -> User:
        if await self.repository.get_user_by_email(user.email) is not None:
            raise EmailExistsException()

        if await self.repository.get_user_by_short_name(user.short_name) is not None:
            raise ShortNameExistsException()

        return await self.repository.create_user(user)

    async def edit_user_info(self, user: User, user_edit: UserEdit) -> User:
        return await self.repository.edit_info(user, user_edit)

    async def edit_user_password(self, user: User, password: str) -> None:
        return await self.repository.edit_password(user, password)

    async def change_admin_status(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.change_admin_status(user)

    async def change_verified_status(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.change_verified_status(user)

    async def change_active_status(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.change_active_status(user)

    async def delete_user(self, user: User) -> None:
        return await self.repository.delete_user(user)

    async def delete_user_by_id(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.delete_user(user)

    async def remove_user_admin_status(self, user_id: int) -> None:
        return await self.repository.remove_user_admin_status(user_id)

    async def remove_admin_status_for_all(self) -> None:
        return await self.repository.remove_admin_status_for_all()

    async def delete_all_users(self) -> None:
        return await self.repository.delete_all_users()
