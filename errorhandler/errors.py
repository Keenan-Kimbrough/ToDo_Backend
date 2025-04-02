from flask import jsonify
from flask_limiter.errors import RateLimitExceeded

def register_error_handlers(app):
    @app.errorhandler(RateLimitExceeded)
    def ratelimit_handler(e):
        return jsonify({
            "error": "Too Many Requests",
            "message": "You have exceeded your allowed number of requests. Please try again later."
        }), 429