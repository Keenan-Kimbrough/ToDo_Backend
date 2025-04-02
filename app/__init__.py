# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, cors
from .auth.routes import auth_bp
from .todos.routes import todos_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todos_bp, url_prefix='/todos')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app