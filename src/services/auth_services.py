from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from src.repositories.auth_repository import UserRepository
from src.models.user_model import Users


MESSAGE_409 = "Duplicate values are not accepted"
MESSAGE_403 = "Accessing denied"
MESSAGE_404 = "User(s) not found"


class AuthService:
    @staticmethod
    def get_user_by_id(db, user, user_id):
        if user["id"] != user_id and  user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)

        user_model = UserRepository.get_user_by_id(db, user_id)

        if user_model is None:
            raise HTTPException(status_code=404, detail=MESSAGE_404)

        return user_model


    @staticmethod
    def register_user(db, user_request, bcrypt_context):
        new_user = Users(\
            username=user_request.username,
            first_name=user_request.first_name.title(),
            last_name=user_request.last_name.title(),
            date_of_birth=user_request.date_of_birth,
            email_address=user_request.email_address,
            hash_password=bcrypt_context.hash(user_request.password),
            role="user",
            is_active=True
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
    def update_user_password(db, user, user_request, user_id, bcrypt_context):
        if user["id"] != user_id and user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)

        user_model = UserRepository.get_user_by_id(db, user_id)

        if user_model is None:
            raise HTTPException(status_code=404, detail=MESSAGE_404)
        
        if not bcrypt_context.verify(user_request.old_password, user_model.hash_password):
            raise HTTPException(status_code=401, detail="Invalid old password")
        
        user_model.hash_password = bcrypt_context.hash(user_request.new_password)

        db.commit()


    @staticmethod
    def update_user_by_id(db, user, user_request, user_id):
        if user["id"] != user_id and user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail=MESSAGE_403)

        user_model = UserRepository.get_user_by_id(db, user_id)

        if user_model is None:
            raise HTTPException(status_code=404, detail=MESSAGE_404)
        
        try:
            for field, value in user_request.model_dump(exclude_unset=True).items():
                setattr(user_model, field, value)

            db.commit()

        except IntegrityError:
            db.rollback()
            
            raise HTTPException(status_code=409, detail=MESSAGE_409)
        
        return user_model


    @staticmethod
    def authenticate_user(username: str, password: str, db, bcrypt_context):
        user = UserRepository.get_user_by_username(db, username)

        if not user:
            return False
        if not bcrypt_context.verify(password, user.hash_password):
            return False
        
        return user