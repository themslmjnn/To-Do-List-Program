from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from typing import Annotated

from db.database import Base

int_pk = Annotated[int, mapped_column(primary_key=True)]

class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int_pk]
    title: Mapped[str]
    deadline: Mapped[date]
    description: Mapped[str]
    priority: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        UniqueConstraint('title', 'deadline', name="uix_title_deadline"),
    )