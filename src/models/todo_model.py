from sqlalchemy import UniqueConstraint, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum
from datetime import date, datetime

from db.database import Base
from src.utils.models_constants import int_pk


class TodoPriority(str, Enum):
    very_high = "very high"
    high = "high"
    medium = "medium"
    low = "low"

class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int_pk]

    title: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    deadline: Mapped[date] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(100))

    priority: Mapped[TodoPriority] = mapped_column(SQLEnum(TodoPriority), index=True, nullable=False)
    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("Users", back_populates="todos")

    __table_args__ = (
        UniqueConstraint('title', 'deadline', name="uix_title_deadline"),
    )