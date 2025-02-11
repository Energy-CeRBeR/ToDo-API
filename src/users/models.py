import datetime

from enum import Enum
from typing import Dict, Any, List

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

from src.tasks.models import Task
from src.categories.models import Category


class Gender(Enum):
    male = "male"
    female = "female"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    short_name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    gender: Mapped[Gender] = mapped_column(default=Gender.male, nullable=False)
    base_category_id: Mapped[int] = mapped_column(default=-1, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now(), nullable=False)

    categories: Mapped[List["Category"]] = relationship(back_populates="user", uselist=True, lazy="selectin",
                                                        cascade="all, delete-orphan")
    tasks: Mapped[List["Task"]] = relationship(back_populates="user", uselist=True, lazy="selectin",
                                               cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "short_name": self.short_name,
            "email": self.email,
            "gender": self.gender.value,
            "base_category_id": int,
            "is_admin": self.is_admin,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "categories": [category.to_dict() for category in self.categories],
            "tasks": [task.to_dict() for task in self.tasks],
        }


class VerifyCode(Base):
    __tablename__ = "verify_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
