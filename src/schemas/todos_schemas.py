from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from src.models.todo_model import TodoPriority
from src.schemas.base_schema import BaseSchema


class TodoBase(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    deadline: date
    description: Optional[str] = Field(max_length=100, default=None)

    priority: TodoPriority
    is_completed: bool


class TodoCreatePublic(TodoBase):
    pass


class TodoCreateAdmin(TodoBase):
    owner_id: int


class TodoResponse(TodoBase, BaseSchema):
    id: int

    owner_id: int


class TodoSearch(BaseModel):
    title: Optional[str] = Field(None, max_length=30)
    deadline: Optional[date] = Field(None)
    description: Optional[str] = Field(None, max_length=50)
    priority: Optional[str] = Field(None, max_length=10)
    is_completed: Optional[bool] = Field(None)


class TodoUpdatePublic(TodoSearch):
    pass


class TodoUpdateAdmin(TodoSearch):
    pass