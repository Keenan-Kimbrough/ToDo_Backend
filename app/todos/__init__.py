# app/todos/__init__.py
from flask import Blueprint

todos_bp_v1 = Blueprint('todos', __name__, url_prefix='api/v1')

from . import routes  # Import routes to register endpoints