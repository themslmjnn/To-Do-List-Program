from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from repositories.auth_repository import UserRepository
from repositories.todos_repository import TodoRepository
from models.todo_model import Todos
from models.user_model import Users


MESSAGE_409 = "Duplicate values are not accepted"
MESSAGE_403 = "Accessing denied"
MESSAGE_404 = "User(s) not found"


class AdminService:
    @staticmethod
    def get_user_by_id(db, user, user_id):
        if user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)

        user_model = UserRepository.get_user_by_id(db, user_id)

        if user_model is None:
            raise HTTPException(status_code=404, detail=MESSAGE_404)

        return user_model
    

    @staticmethod
    def get_all_users(db, user):
        if user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)
        
        return UserRepository.get_all_users(db)


    @staticmethod
    def register_user(db, user, user_request, bcrypt_context):
        if user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)
    
        new_user = Users(\
            username=user_request.username,
            first_name=user_request.first_name.title(),
            last_name=user_request.last_name.title(),
            date_of_birth=user_request.date_of_birth,
            email_address=user_request.email_address,
            hash_password=bcrypt_context.hash(user_request.password),
            role=user_request.role,
            is_active=user_request.is_active
        )

        try:
            UserRepository.add_user(db, new_user)

            db.commit()
            db.refresh(new_user)

            return new_user
        
        except IntegrityError:
            db.rollback()

            raise HTTPException(status_code=409, detail=MESSAGE_409)


    @staticmethod
    def delete_user_by_id(db, user, user_id):
        if user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)

        user_model = UserRepository.get_user_by_id(db, user_id)

        if user_model is None:
            raise HTTPException(status_code=404, detail=MESSAGE_404)
        
        UserRepository.delete_user_by_id(db, user_model)

        db.commit()


    @staticmethod
    def get_all_todos(db, user):
        if user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)
    
        return TodoRepository.get_all_todos(db)
    

    @staticmethod
    def search_todos(db, user, search_request):
        if user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)
        
        todo_model = TodoRepository.search_todo(db, search_request)

        if not todo_model:
            raise HTTPException(status_code=404, detail=MESSAGE_404)
        
        return todo_model
    
    
    @staticmethod
    def add_todo_admin(db, user, todo_request):
        if user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)
        
        todo_model = Todos(**todo_request.model_dump())

        try:
            TodoRepository.add_todo(db, todo_model)
            
            db.commit()
            db.refresh(todo_model)

            return todo_model
        
        except IntegrityError:
            db.rollback()

            raise HTTPException(status_code=409, detail=MESSAGE_409)