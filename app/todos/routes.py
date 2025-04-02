# app/todos/routes.py
from flask import jsonify, request
from . import todos_bp
from app.models import Todo
from app.extensions import db
from app import limiter

@todos_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
def get_todos():
    current_app.logger.info('Fetching all todos')
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@todos_bp.route('/', methods=['POST'])
@limiter.limit("7 per minute")
def add_todo():
    current_app.logger.info('Creating todos')
    data = request.get_json()
    todo = Todo(text=data['text'], completed=False)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
@limiter.limit("10 per minute")
def delete_todo(todo_id):
    current_app.logger.info('Deleteing  todos')
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Todo not found'}), 404