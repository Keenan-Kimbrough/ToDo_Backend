# app/todos/routes.py
from flask import jsonify, request
from . import todos_bp_v1
from app.models import Todo
from app.extensions import db
from app import limiter
from app.schema import TodoSchema
from app.resourceSupport import syntatical_validation_of_to_do

todo_schema = TodoSchema() # single objects schema
todos_schema = Todoschema(many=True) # for lists

@todos_bp_v1.route('/', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)  # Cache this route for 60 seconds
def get_todos():
    current_app.logger.info('Fetching all todos')
    todos = Todo.query.all()
    response = jsonify([todo.to_dict() for todo in todos])
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response

@todos_bp_v1.route('/', methods=['POST'])
@limiter.limit("7 per minute")
def add_todo():
    current_app.logger.info('Creating todos')
    response = ''
    data = request.get_json()
    if not data:
        return jsonify({"message":"no input data provided"}),400

    # validate and deserialize input
    isvalid = syntatical_validation_of_to_do(data)

    if not isvalid:
        response = ({"message": "No input data provided"})
        return response, 422

    data = todo_schema.load(data)
   
    todo = Todo(text=data['text'], completed=False)
    db.session.add(todo)
    db.session.commit()

    todo = todo_schema.dump(todo)
    response = jsonify(todo)
    return response, 201

@todos_bp_v1.route('/<int:todo_id>', methods=['DELETE'])
@limiter.limit("10 per minute")
def delete_todo(todo_id):
    current_app.logger.info('Deleteing  todos')
    todo = Todo.query.get(todo_id)
    response = ''
    if todo:
        db.session.delete(todo)
        db.session.commit()
        response = jsonify({'successfully deleted todo_id: ${todo_is}'})
        return response, 204
    response =jsonify({'error': 'Todo not found'})
    return response, 404