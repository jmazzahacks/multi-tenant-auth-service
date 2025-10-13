"""
Authentication middleware for protecting routes.
"""
from functools import wraps
from flask import request, jsonify
from services.token_service import token_service


def require_auth(func):
    """
    Decorator to require authentication for a route.
    Extracts the auth token from the Authorization header and validates it.

    Sets request.user_id with the authenticated user's ID.

    Returns 401 if token is missing or invalid.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401

        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header format'}), 401

        token = auth_header[7:]  # Remove 'Bearer ' prefix

        user_id = token_service.validate_auth_token(token)

        if user_id is None:
            return jsonify({'error': 'Invalid or expired token'}), 401

        request.user_id = user_id
        return func(*args, **kwargs)

    return wrapper
