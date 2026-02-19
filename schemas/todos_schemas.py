from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TodoBase(BaseModel):
    title: str = Field(min_length=5, max_length=30)
    deadline: date
    description: Optional[str] = Field(max_length=50, default=None)
    priority: str = Field(min_length=3, max_length=10)
    is_completed: bool = Field(default=False)

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int

    class Config:
        from_attributes = True

class TodoSearch(BaseModel):
    title: Optional[str] = Field(None, max_length=30)
    deadline: Optional[date] = Field(None)
    description: Optional[str] = Field(None, max_length=50)
    priority: Optional[str] = Field(None, max_length=10)
    is_completed: Optional[bool] = Field(None)

class TodoUpdate(TodoSearch):
    pass