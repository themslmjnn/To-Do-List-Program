from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from typing import Annotated

from db.database import Base


int_pk = Annotated[int, mapped_column(primary_key=True)]

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