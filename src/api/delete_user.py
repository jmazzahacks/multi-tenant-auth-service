"""
Delete user endpoint.
"""
from flask import Blueprint, jsonify
from database import Database
from utils.api_key_middleware import require_master_api_key

delete_user_bp = Blueprint('delete_user', __name__)


@delete_user_bp.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@require_master_api_key
def delete_user(user_id: int):
    """
    Delete a user and all associated data.

    Requires master API key (X-API-Key header).

    Path parameters:
        user_id: User ID to delete

    Returns:
        200: User deleted successfully
        401: Missing or invalid API key
        404: User not found
    """
    db = Database()

    # Check if user exists first
    user = db.find_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    deleted = db.delete_user(user_id)
    if deleted:
        return jsonify({'message': f'User {user_id} deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete user'}), 500
