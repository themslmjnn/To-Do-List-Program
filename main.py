from fastapi import FastAPI
from db.database import sync_engine
from routers import todos, auth

import models.models as models

app = FastAPI(title="To-Do List Program")

app.include_router(todos.router)
app.include_router(auth.router)

models.Base.metadata.create_all(bind=sync_engine)