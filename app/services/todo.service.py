from app.models import Todo
from app.extensions import db
from app.schemas.todo_schema import Todoschema
from marshmallow import ValidationError

todo_schema = TodoSchema()
class TodoService:
    def create_todo(self,data):
        """
        Validates input data and creates a new Todo.
        Raise validation error if data is invalid
        
        """
        todo = todo_schema.load(data)
        isvalid = self.to_do_semantic_validation(todo)

        todo = TodoRepository.create_todo(
        text=validated_data['text'],
        completed=validated_data.get('completed', False)
    )
    return todo_schema.dump(todo)

    # Semantic validation 
    def to_do_semantic_validation(todo):
        if Todo.query.filter_by(text=validation_data['text']).first():
            raise ValueError("A Todo with that text already exists")
        else:
            return True


    # creae todo and persit the todo