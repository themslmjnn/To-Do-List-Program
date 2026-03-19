from sqlalchemy import func, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date, datetime
from enum import Enum

from db.database import Base
from src.utils.models_constants import int_pk


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))

    date_of_birth: Mapped[date] = mapped_column(nullable=False)

    email_address: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), index=True, nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    todos = relationship("Todo", back_populates="user")