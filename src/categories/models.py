import datetime

from typing import Dict, Any, List
from sqlalchemy import func, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(default="#FFFFFF", nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="categories", uselist=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="category", uselist=True, lazy="selectin",
                                               cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "tasks": [task.to_dict() for task in self.tasks],
        }
