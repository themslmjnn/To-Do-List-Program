from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_

from models.todo_model import Todos


class TodoRepository:
    @staticmethod
    def get_all_todos(db: Session):
        query = select(Todos)

        result = db.execute(query)

        return result.scalars().all()
    

    @staticmethod
    def get_todo_by_user_id(db: Session, user_id: int):
        query = (
            select(Todos)
            .filter(Todos.user_id == user_id)
        )

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

        return new_todo
    
    
    @staticmethod
    def delete_todo(db: Session, todo_model):
        db.delete(todo_model)


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
            query = query.filter(Todos.priority == todo.priority)

        if todo.is_completed is not None:
            query = query.filter(Todos.is_completed == todo.is_completed)

        result = db.execute(query)

        return result.scalars().all()
    

    @staticmethod
    def get_user_id_by_todo_id(db: Session, todo_id):
        query = (
            select(Todos.user_id)
            .filter(Todos.id == todo_id)
        )

        result = db.execute(query)

        return result.scalars().first()