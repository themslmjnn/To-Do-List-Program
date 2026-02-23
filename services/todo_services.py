from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from repositories.todos_repository import TodoRepository
from models.todo_model import Todos


MESSAGE_404 = "Todo(s) not found"
MESSAGE_403 = "Access denied"
MESSAGE_409 = "Duplicate values are not accepted"


class TodoService:
    @staticmethod
    def get_todos_by_user_id(db, user, user_id):        
        todo_model = TodoRepository.get_todo_by_user_id(db, user_id)

        if todo_model is None:
            raise HTTPException(status_code=404, detail=MESSAGE_404)
        
        if user["id"] != user_id and user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)
        
        return todo_model
    

    @staticmethod
    def add_todo(db, user, todo_request):        
        todo_model = Todos(**todo_request.model_dump(), user_id = user["id"])

        try:
            TodoRepository.add_todo(db, todo_model)

            db.commit()
            db.refresh(todo_model)

            return todo_model
        
        except IntegrityError:
            db.rollback()

            raise HTTPException(status_code=409, detail=MESSAGE_409)
        

    @staticmethod
    def delete_todo_by_id(db, user, todo_id):
        if user["id"] != TodoRepository.get_user_id_by_todoid(db, todo_id) and user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)
        
        todo_model = TodoRepository.get_todo_by_id(db, todo_id)

        if todo_model is None:
            raise HTTPException(status_code=404, detail=MESSAGE_404)
        
        TodoRepository.delete_todo(db, todo_model)

        db.commit()


    @staticmethod
    def update_todo_by_id(db, user, todo_request, todo_id):
        todo_model = TodoRepository.get_todo_by_id(db, todo_id)

        if user["id"] !=  todo_model.user_id and user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)

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
