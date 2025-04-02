from marshmallow import Schema, fields, validate, ValidationError

class TodoSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True, validate=validate.Length(min=1, error="Text cannot be empty."))
    completed = fields.Bool(required=False)