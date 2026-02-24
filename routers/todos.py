from fastapi import APIRouter, Depends, Path

from sqlalchemy.orm import Session

from typing import Annotated

from starlette import status

from db.database import get_db
from core.security import get_current_user
from schemas.todos_schemas import TodoCreatePublic, TodoResponse, TodoUpdate
from services.todo_services import TodoService


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]
    

@router.get("/users/{user_id}/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos_by_user_id(
        db: db_dependency,
        user: user_dependency, 
        user_id: Annotated[int, Path(ge=1)]):
    
    return TodoService.get_todos_by_user_id(db, user, user_id)


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def add_todos(
        db: db_dependency,
        user: user_dependency,
        todo_request: TodoCreatePublic):
    
    return TodoService.add_todo(db, user, todo_request)
    

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(
    db: db_dependency,
    user: user_dependency, 
    todo_id: Annotated[int, Path(ge=1)]):

    TodoService.delete_todo_by_id(db, user, todo_id)


@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo_by_id(
    db: db_dependency,
    user: user_dependency, 
    todo_request: TodoUpdate, 
    todo_id: Annotated[int, Path(ge=1)]):
    
    return TodoService.update_todo_by_id(db, user, todo_request, todo_id)

