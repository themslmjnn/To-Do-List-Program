from sqlalchemy import UniqueConstraint, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import Annotated

from db.database import Base
from enum import Enum

int_pk = Annotated[int, mapped_column(primary_key=True)]

class TodoPriority(str, Enum):
    very_high = "very high"
    high = "high"
    medium = "medium"
    low = "low"

class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int_pk]
    title: Mapped[str]
    deadline: Mapped[date]
    description: Mapped[str]
    priority: Mapped[TodoPriority] = mapped_column(SQLEnum(TodoPriority))
    is_completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["Users"] = relationship("Users",back_populates="todos")

    __table_args__ = (
        UniqueConstraint('title', 'deadline', name="uix_title_deadline"),
    )