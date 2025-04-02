from app.extensions import db
from app.models import Todo

class TodoRepository:
    @staticmethod
    def create_todo(text, completed=False):
        todo = Todo(text=text, completed=completed)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def get_all_todos():
        return Todo.query.all()

    @staticmethod
    def get_todo_by_id(todo_id):
        return Todo.query.get(todo_id)

    @staticmethod
    def update_todo(todo):
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo_id):
        todo = Todo.query.get(todo_id)
        if todo:
            db.session.delete(todo)
            db.session.commit()
        return todo