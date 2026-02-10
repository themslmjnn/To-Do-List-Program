from fastapi import FastAPI
from database import engine
from routers import todos, auth

import models

app = FastAPI(title="To-Do List Program")

app.include_router(todos.router)
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)