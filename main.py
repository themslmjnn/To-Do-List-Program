from fastapi import FastAPI
from routers import todos, auth, admin

import models as models

app = FastAPI(title="To-Do List Program")

app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(admin.router)
