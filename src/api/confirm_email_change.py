"""
Confirm email change endpoint.
"""
from flask import Blueprint, jsonify
from services.auth_service import auth_service
from schemas.auth_schemas import ConfirmEmailChangeSchema, UserResponseSchema
from utils.validators import validate_request

confirm_email_change_bp = Blueprint('confirm_email_change', __name__)


@confirm_email_change_bp.route('/api/auth/confirm-email-change', methods=['POST'])
@validate_request(ConfirmEmailChangeSchema)
def confirm_email_change(validated_data):
    """
    Confirm an email change using a confirmation token.

    Request body:
        token: Email change confirmation token

    Returns:
        200: Email changed successfully
        400: Invalid or expired token
    """
    try:
        user = auth_service.confirm_email_change(validated_data['token'])
        schema = UserResponseSchema()
        return jsonify(schema.dump(user)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
