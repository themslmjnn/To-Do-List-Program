from fastapi import APIRouter, Depends, HTTPException, Path, Query
from database import get_db
from pydantic_schemas import TodoCreate, TodoResponse
from typing import Annotated, Optional
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date
from sqlalchemy import func

import models


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK, tags=["Get Methods"])
async def get_all_todos(db: db_dependency):
    return db.query(models.Todos).all()


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
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo_model
    

@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK, tags=["Search Methods"])
async def get_books_by_id(db: db_dependency, todo_id: int = Path(ge=1)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo_model


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, tags=["Add Methods"])
async def add_todos(db: db_dependency, todo_request: TodoCreate):
    todo_model = models.Todos(**todo_request.model_dump())

    try:
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)

        return todo_model
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail="Duplicate values are not accepted")
    

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Delete Methods"])
async def delete_todo_by_id(db: db_dependency, todo_id: int = Path(ge=1)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo_model)
    db.commit()

@router.put("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK, tags=["Update Methods"])
async def update_todos_by_id(db: db_dependency, todo_request: TodoCreate, todo_id: int = Path(ge=1)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    try:
        for field, value in todo_request.model_dump().items():
            setattr(todo_model, field, value)

        db.commit()
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail="Duplicate values are not accepted")
    
    return todo_model