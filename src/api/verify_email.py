"""
Email verification endpoint.
"""
from flask import Blueprint, jsonify
from services.auth_service import auth_service
from schemas.auth_schemas import VerifyEmailRequestSchema, UserResponseSchema
from utils.validators import validate_request

verify_email_bp = Blueprint('verify_email', __name__)


@verify_email_bp.route('/api/auth/verify-email', methods=['POST'])
@validate_request(VerifyEmailRequestSchema)
def verify_email(validated_data):
    """
    Verify a user's email address.

    Request body:
        token: Email verification token

    Returns:
        200: Email verified successfully
        400: Invalid or expired token
    """
    try:
        user = auth_service.verify_email(validated_data['token'])
        schema = UserResponseSchema()
        return jsonify(schema.dump(user)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
