"""
Resend verification email endpoint.
"""
from flask import Blueprint, jsonify, request
from services.auth_service import auth_service
from utils.api_key_middleware import require_master_api_key

resend_verification_bp = Blueprint('resend_verification', __name__)


@resend_verification_bp.route('/api/admin/resend-verification/<int:user_id>', methods=['POST'])
@require_master_api_key
def resend_verification(user_id: int):
    """
    Resend verification email for a user.

    Requires master API key (X-API-Key header).

    Path parameters:
        user_id: User ID

    Returns:
        200: Verification email sent successfully
        400: User already verified or email failed
        401: Missing or invalid API key
        404: User not found
    """
    try:
        success = auth_service.resend_verification_email(user_id)
        if success:
            return jsonify({'message': 'Verification email sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send verification email'}), 400
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg.lower():
            return jsonify({'error': error_msg}), 404
        return jsonify({'error': error_msg}), 400
