from app.schema import TodoSchema

def syntatical_validation_of_to_do(todo):
    errors = todo_schema.validate(data)
    return errors 