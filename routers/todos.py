from fastapi import APIRouter, Depends, HTTPException, Path, Query
from db.database import get_db
from schemas.pydantic_schemas import TodoCreate, TodoResponse
from typing import Annotated, Optional
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date
from sqlalchemy import func
from .auth import get_current_user
from repositories import todos_repository

import models.models as models


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

MESSAGE_404 = "Todo(s) not found"
MESSAGE_409 = "Duplicate values are not accepted"

@router.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK, tags=["Get Methods"])
def get_all_todos(db: db_dependency):
    return todos_repository.SyncORM.get_all_todos(db)


@router.get("/todos/search", response_model=list[TodoResponse], status_code=status.HTTP_200_OK, tags=["Search Methods"])
async def search_books(db: db_dependency, 
                       title: Optional[str] = Query(default=None),
                       deadline: Optional[date] = Query(default=None),
                       description: Optional[str] = Query(max_length=50, default=None),
                       priority: Optional[str] = Query(max_length=10, default=None),
                       is_completed: Optional[bool] = Query(default=None)
                       ):
    
    query = db.query(models.Todos)

    if title:
        query = query.filter(func.lower(models.Todos.title).contains(title.lower()))

    if deadline:
        query = query.filter(models.Todos.deadline == title)

    if description:
        query = query.filter(func.lower(models.Todos.description).contains(description.lower()))

    if priority:
        query = query.filter(func.lower(models.Todos.priority).contains(priority.lower()))

    if is_completed:
        query = query.filter(func.lower(models.Todos.is_completed).contains(is_completed.lower()))

    todo_model = query.all()

    if not todo_model:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    return todo_model
    

@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK, tags=["Search Methods"])
async def get_todos_by_id(db: db_dependency, todo_id: int = Path(ge=1)):
    todo_model = todos_repository.SyncORM.get_todo_by_id(db, todo_id)

    if todo_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    return todo_model


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, tags=["Add Methods"])
async def add_todos(user: user_dependency, db: db_dependency, todo_request: TodoCreate):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed Authentication")
    
    todo_model = models.Todos(**todo_request.model_dump())

    try:
        return todos_repository.SyncORM.add_todo(db, todo_model)
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail=MESSAGE_409)
    

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Delete Methods"])
async def delete_todo_by_id(db: db_dependency, todo_id: int = Path(ge=1)):
    todo_model = todos_repository.SyncORM.get_todo_by_id(db, todo_id)

    if todo_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    todos_repository.SyncORM.delete_todo(db, todo_model)

@router.put("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK, tags=["Update Methods"])
async def update_todos_by_id(db: db_dependency, todo_request: TodoCreate, todo_id: int = Path(ge=1)):
    todo_model = todos_repository.SyncORM.get_todo_by_id(db, todo_id)

    if todo_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    try:
        for field, value in todo_request.model_dump().items():
            setattr(todo_model, field, value)

        db.commit()
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail=MESSAGE_409)
    
    return todo_model