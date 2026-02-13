from pydantic import BaseModel, Field, EmailStr
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

class UserBase(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    date_of_birth: date
    email_address: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=6)
    role: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=False)

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str