# app/auth/routes.py
from flask import jsonify, request, make_response
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import current_app  # Use current_app to access config
from . import auth_bp

# Dummy user data for demonstration
USER = {"id": 1, "username": "testuser", "password": "password123"}

ACCESS_TOKEN_EXPIRY = 15  # minutes
REFRESH_TOKEN_EXPIRY = 7   # days

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except Exception as e:
            return jsonify({"message": "Token is invalid", "error": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def generate_access_token(user):
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    token = jwt.encode({'user': user, 'exp': expiry}, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def generate_refresh_token(user):
    expiry = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRY)
    token = jwt.encode({'user': user, 'exp': expiry}, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and data.get('username') == USER['username'] and data.get('password') == USER['password']:
        access_token = generate_access_token({"id": USER["id"], "username": USER["username"]})
        refresh_token = generate_refresh_token({"id": USER["id"], "username": USER["username"]})
        response = make_response(jsonify({'access_token': access_token}))
        # Set refresh token as an HttpOnly, Secure cookie
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Strict')
        return response
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 401
    try:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user = data['user']
        new_access_token = generate_access_token(user)
        return jsonify({'access_token': new_access_token})
    except Exception as e:
        return jsonify({'message': 'Refresh token is invalid', 'error': str(e)}), 401