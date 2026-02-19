from fastapi import FastAPI
from db.database import sync_engine, Base
from routers import todos, auth, test

import models as models

app = FastAPI(title="To-Do List Program")

app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(test.router)

Base.metadata.create_all(bind=sync_engine)
