# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, cors
from .auth.routes import auth_bp
from .todos.routes import todos_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
        # Configure logging: log to both console and a file.
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(app.root_path, 'app.log'),
                'formatter': 'default'
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'file']
        }
    })







    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)

    # Set up Prometheus monitoring
    metrics = PrometheusMetrics(app)
    # Optional: register default counters for requests, etc.
    metrics.register_default(
        metrics.counter(
            'app_request_count', 'Total Request Count',
            labels={'method': lambda: request.method, 'endpoint': lambda: request.path}
        )
    )


    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todos_bp, url_prefix='/todos')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app