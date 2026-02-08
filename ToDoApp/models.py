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