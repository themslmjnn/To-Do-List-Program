from models import models
from sqlalchemy.orm import Session

class SyncORM:
    @staticmethod
    def get_all_todos(db: Session):
        return db.query(models.Todos).all()
    
    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int):
        return db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    @staticmethod
    def add_todo(db: Session, new_todo):
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        return new_todo
    
    @staticmethod
    def delete_todo(db: Session, todo_model):
        db.delete(todo_model)
        db.commit()
        
