"""
User logout endpoint.
"""
from flask import Blueprint, jsonify, request
from database import db_manager
from utils.auth_middleware import require_auth

logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """
    Logout a user by invalidating their auth token.

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: Logout successful
        401: Missing or invalid token
        404: Token not found
    """
    auth_header = request.headers.get('Authorization')
    token = auth_header[7:]  # Remove 'Bearer ' prefix

    deleted = db_manager.delete_auth_token(token)

    if deleted:
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'error': 'Token not found'}), 404
