import datetime

from enum import Enum
from typing import Dict, Any
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000))
    priority: Mapped[Priority] = mapped_column(default=Priority.MEDIUM, nullable=False)
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)

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
            "date": self.date.isoformat()
        }
