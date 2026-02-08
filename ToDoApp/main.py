from fastapi import FastAPI, Depends
from database import engine, get_db
from pydantic_schemas import TodoCreate, TodoResponse
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session

import models

app = FastAPI(title="To-Do List Program")

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK, tags=["Get Todos"])
async def get_all_todos(db: db_dependency):
    return db.query(models.Todos).all()