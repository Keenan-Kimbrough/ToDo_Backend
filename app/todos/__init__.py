# app/todos/__init__.py
from flask import Blueprint

todos_bp = Blueprint('todos', __name__)

from . import routes  # Import routes to register endpoints