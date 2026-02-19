from models.user_model import Users
from sqlalchemy.orm import Session
from sqlalchemy import select

class UserRepository:
    @staticmethod
    def get_all_users(db: Session):
        query = select(Users)

        result = db.execute(query)

        return result.scalars().all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        query = (
            select(Users)
            .filter(Users.id == user_id)
        )

        result = db.execute(query)

        return result.scalars().first()
    
    @staticmethod
    def delete_user_by_id(db: Session, user_model):
        db.delete(user_model)
        db.commit()

    @staticmethod
    def add_user(db: Session, new_user):
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        query = (
            select(Users)
            .filter(Users.username == username)
        )

        result = db.execute(query)

        return result.scalars().first()
