from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime

from src.models.user_model import UserRole
from src.schemas.base_schema import BaseSchema


class UserBase(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    date_of_birth: date
    email_address: EmailStr


class UserCreatePublic(UserBase):
    password: str = Field(min_length=8)


class UserResponsePublic(UserBase, BaseSchema):
    id: int

    role: UserRole
    is_active: bool


class UserCreateAdmin(UserBase):
    password: str = Field(min_length=8)

    role: UserRole
    is_active: bool


class UserResponseAdmin(UserBase, BaseSchema):
    id: int

    role: UserRole
    is_active: bool

    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=20)
    first_name: Optional[str] = Field(None, min_length=2, max_length=20)
    last_name: Optional[str] = Field(None, min_length=2, max_length=20)
    date_of_birth: Optional[date] = Field(None)
    email_address: Optional[EmailStr] = Field(None)


class UserUpdatePassword(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)


class UserSearch(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    date_of_birth: Optional[date] = None

    role: Optional[UserRole] = None
    
    is_active: Optional[bool] = None


class CurrentUserResponse(BaseSchema):
   id: int

   username: str = Field(min_length=6, max_length=20)

   role: UserRole