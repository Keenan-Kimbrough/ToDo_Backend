from app.models import Todo
from app.extensions import db
from app.schemas.todo_schema import Todoschema
from marshmallow import ValidationError

todo_schema = TodoSchema()

def create_todo(data):
    """
    Validates input data and creates a new Todo.
    Raise validation error if data is invalid
    
    """

    # Semantic validation 
    def semantic_validation(todo):
        if Todo.query.filter_by(text=validation_data['text']).first():
            raise ValueError("A Todo with that text already exists")


    # creae todo and persit the todo