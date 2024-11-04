import datetime

from enum import Enum
from typing import Dict, Any, List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

from src.tasks.models import Task
from src.categories.models import Category


class Roles(Enum):
    user = "user"
    admin = "admin"


class Gender(Enum):
    male = "male"
    female = "female"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    short_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    gender: Mapped[Gender] = mapped_column(default=Gender.male)
    role: Mapped[Roles] = mapped_column(default=Roles.user)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    password_hash: Mapped[bytes] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

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
            "role": self.role.value,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "categories": [category.to_dict() for category in self.categories],
            "tasks": [task.to_dict() for task in self.tasks],
        }
