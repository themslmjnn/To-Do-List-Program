from models import models
from sqlalchemy.orm import Session

class AuthRepo:
    @staticmethod
    def get_all_users(db: Session):
        return db.query(models.Users).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(models.Users).filter(models.Users.id == user_id).first()
    
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
        return db.query(models.Users).filter(models.Users.username == username).first()
