from models.todo_model import Todos
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_

class TodoRepository:
    @staticmethod
    def get_all_todos(db: Session):
        query = select(Todos)

        result = db.execute(query)

        return result.scalars().all()
    
    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int):
        query = (
            select(Todos)
            .filter(Todos.id == todo_id)
        )

        result = db.execute(query)

        return result.scalars().first()
    
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

    @staticmethod
    def search_todo(db: Session, todo):
        query = select(Todos)

        if todo.title:
            query = query.filter(func.lower(Todos.title).contains(todo.title.lower()))

        if todo.deadline:
            query = query.filter(Todos.deadline == todo.deadline)

        if todo.description:
            query = query.filter(func.lower(Todos.description).contains(todo.description.lower()))

        if todo.priority:
            query = query.filter(func.lower(Todos.priority).contains(todo.priority.lower()))

        if todo.is_completed is not None:
            query = query.filter(Todos.is_completed == todo.is_completed)

        result = db.execute(query)

        return result.scalars().all()