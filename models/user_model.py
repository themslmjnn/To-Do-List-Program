from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import Annotated

from db.database import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum

int_pk = Annotated[int, mapped_column(primary_key=True)]


class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email_address: Mapped[str] = mapped_column(unique=True)
    hash_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole))
    is_active: Mapped[bool] = mapped_column(default=True)
    todos: Mapped[list["Todos"]] = relationship("Todos", back_populates="owner", cascade="all, delete")