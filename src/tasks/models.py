import datetime

from enum import Enum
from typing import Dict, Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    priority: Mapped[Priority] = mapped_column(default=Priority.MEDIUM)
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="tasks", uselist=False)
    category: Mapped["Category"] = relationship(back_populates="tasks", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat()
        }
