"""
User registration endpoint.
"""
from flask import Blueprint, jsonify
from services.auth_service import auth_service
from schemas.auth_schemas import RegisterRequestSchema, UserResponseSchema
from utils.validators import validate_request

register_bp = Blueprint('register', __name__)


@register_bp.route('/api/auth/register', methods=['POST'])
@validate_request(RegisterRequestSchema)
def register(validated_data):
    """
    Register a new user.

    Request body:
        site_id: ID of the site
        email: User email
        password: User password (min 8 characters)

    Returns:
        201: User created successfully
        400: Validation error or duplicate email
    """
    try:
        user = auth_service.register_user(
            site_id=validated_data['site_id'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        schema = UserResponseSchema()
        return jsonify(schema.dump(user)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
