import datetime

from enum import Enum
from typing import Dict, Any

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Colors(Enum):
    RED = "#F44336"  # Красный
    GREEN = "#4CAF50"  # Зеленый
    BLUE = "#2196F3"  # Синий
    YELLOW = "#FFC107"  # Желтый
    ORANGE = "#FF9800"  # Оранжевый
    PURPLE = "#9C27B0"  # Фиолетовый
    PINK = "#E91E63"  # Розовый
    BROWN = "#795548"  # Коричневый
    GREY = "#9E9E9E"  # Серый
    BLACK = "#212121"  # Черный
    WHITE = "#FFFFFF"  # Белый
    CYAN = "#00BCD4"  # Голубой
    LIME = "#C0CA33"  # Лаймовый
    TEAL = "#009688"  # Зелено-голубой
    INDIGO = "#3F51B5"  # Индиго
    DEEP_PURPLE = "#673AB7"  # Темно-фиолетовый
    LIGHT_BLUE = "#03A9F4"  # Светло-голубой
    LIGHT_GREEN = "#8BC34A"  # Светло-зеленый
    LIGHT_GREY = "#EEEEEE"  # Светло-серый
    AMBER = "#FFC107"  # Янтарный
    DEEP_ORANGE = "#FF5722"  # Темно-оранжевый
    LIGHT_PINK = "#F48FB1"  # Светло-розовый


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    color: Mapped[Colors] = mapped_column(default=Colors.BLUE)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
