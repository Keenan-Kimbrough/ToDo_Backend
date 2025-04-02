class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text  db.column(db.String(200), nullable=False)
    completed = db.column(db.Boolean, default=False)
    def to_dict(self):
        return {
            'id': self.id,
            "text": self.text,
            "completed": self.completed
        }