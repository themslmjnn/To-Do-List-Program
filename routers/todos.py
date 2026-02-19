from fastapi import APIRouter, Depends, HTTPException, Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from typing import Annotated

from starlette import status

from db.database import get_db
from core.security import get_current_user
from schemas.todos_schemas import TodoCreate, TodoResponse, TodoUpdate, TodoSearch
from repositories.todos_repository import TodoRepository
from models.todo_model import Todos


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


MESSAGE_404 = "Todo(s) not found"
MESSAGE_409 = "Duplicate values are not accepted"


@router.get("", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_all_todos(db: db_dependency):
    return TodoRepository.get_all_todos(db)


@router.get("/search", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def search_books(db: db_dependency, search_book_request: TodoSearch = Depends()):
    
    todo_model = TodoRepository.search_todo(db, search_book_request)

    if not todo_model:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    return todo_model
    

@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_todos_by_id(db: db_dependency, todo_id: int = Path(ge=1)):
    todo_model = TodoRepository.get_todo_by_id(db, todo_id)

    if todo_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    return todo_model


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def add_todos(user: user_dependency, db: db_dependency, todo_request: TodoCreate):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed Authentication")
    
    todo_model = Todos(**todo_request.model_dump())

    try:
        return TodoRepository.add_todo(db, todo_model)
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail=MESSAGE_409)
    

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(db: db_dependency, todo_id: int = Path(ge=1)):
    todo_model = TodoRepository.get_todo_by_id(db, todo_id)

    if todo_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    TodoRepository.delete_todo(db, todo_model)

@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todos_by_id(db: db_dependency, todo_request: TodoUpdate, todo_id: int = Path(ge=1)):
    todo_model = TodoRepository.get_todo_by_id(db, todo_id)

    if todo_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    try:
        for field, value in todo_request.model_dump(exclude_unset=True).items():
            setattr(todo_model, field, value)

        db.commit()
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail=MESSAGE_409)
    
    return todo_model

