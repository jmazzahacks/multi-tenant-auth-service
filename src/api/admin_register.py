"""
Admin user registration endpoint.
"""
from flask import Blueprint, jsonify
from services.auth_service import auth_service
from models.user_role import UserRole
from schemas.auth_schemas import RegisterRequestSchema, UserResponseSchema
from utils.validators import validate_request
from utils.api_key_middleware import require_master_api_key

admin_register_bp = Blueprint('admin_register', __name__)


@admin_register_bp.route('/api/admin/register', methods=['POST'])
@require_master_api_key
@validate_request(RegisterRequestSchema)
def admin_register(validated_data):
    """
    Register a new admin user for a site.

    Requires master API key (X-API-Key header).

    This endpoint is used to create the first admin for a site or add additional
    site administrators. Only accessible with the master API key.

    Request body:
        site_id: ID of the site
        email: Admin email
        password: Admin password (min 8 characters)

    Returns:
        201: Admin user created successfully
        400: Validation error or duplicate email
        401: Missing or invalid API key
    """
    try:
        user = auth_service.register_user(
            site_id=validated_data['site_id'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=UserRole.ADMIN
        )
        schema = UserResponseSchema()
        return jsonify(schema.dump(user)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
