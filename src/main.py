from fastapi import FastAPI
from src.routers import todos, user_routers

import src.models as models
from src.routers import auth_routers

app = FastAPI(title="To-Do List Program")

app.include_router(todos.router)
app.include_router(auth_routers.router)
app.include_router(user_routers.router)
