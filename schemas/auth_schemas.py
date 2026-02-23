from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    date_of_birth: date
    email_address: EmailStr

class UserCreatePublic(UserBase):
    password: str = Field(min_length=6)

class UserCreateAdmin(UserBase):
    password: str = Field(min_length=6)
    role: str = Field(default="user")
    is_active: bool = Field(default=True)

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=20)
    first_name: Optional[str] = Field(None, min_length=2, max_length=20)
    last_name: Optional[str] = Field(None, min_length=2, max_length=20)
    date_of_birth: Optional[date] = Field(None)
    email_address: Optional[EmailStr] = Field(None)

class UserUpdatePassword(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str