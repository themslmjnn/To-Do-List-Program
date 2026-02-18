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

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email_address: Mapped[str] = mapped_column(unique=True)
    hash_password: Mapped[str]
    role: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)