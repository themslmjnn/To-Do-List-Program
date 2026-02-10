from database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, UniqueConstraint

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    deadline = Column(Date)
    description = Column(String)
    priority = Column(String)
    is_completed = Column(String, default=False)

    __table_args__ = (
        UniqueConstraint('title', 'deadline', name="uix_title_deadline"),
    )

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    email_address = Column(String, unique=True)
    hash_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=False)