from fastapi import APIRouter, Depends, Path, status

from typing import Annotated

from db.database import db_dependency
from src.core.security import user_dependency, bcrypt_context
from src.schemas.todos_schemas import TodoResponse, TodoSearch, TodoCreateAdmin
from src.schemas.user_schemas import UserResponse, UserCreateAdmin
from src.services.user_services import AdminService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(
        db: db_dependency, 
        user: user_dependency):
       
    return AdminService.get_all_users(db, user)


@router.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(
        db: db_dependency, 
        user: user_dependency,
        user_id: Annotated[int, Path(ge=1)]):

    return AdminService.get_user_by_id(db, user, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(
        db: db_dependency, 
        user: user_dependency,
        user_id: Annotated[int, Path(ge=1)]):

    AdminService.delete_user_by_id(db, user, user_id)


@router.post("/user_registration", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_users_admin(
        user: user_dependency,
        db: db_dependency, 
        user_request: UserCreateAdmin):

    return AdminService.register_user(db, user, user_request, bcrypt_context)
    

@router.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_all_todos(
        db: db_dependency,
        user: user_dependency):
    
    return AdminService.get_all_todos(db, user)


@router.get("/todos/search", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def search_todos(
        db: db_dependency, 
        user: user_dependency,
        search_request: Annotated[TodoSearch, Depends()]):
    
    return AdminService.search_todos(db, user, search_request)


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def add_todo_admin(
        db: db_dependency,
        user: user_dependency,
        todo_request: TodoCreateAdmin):
    
    return AdminService.add_todo_admin(db, user, todo_request)