"""
Create site endpoint.
"""
from flask import Blueprint, jsonify
import time
from database import db_manager
from models.site import Site
from schemas.site_schemas import CreateSiteRequestSchema, SiteResponseSchema
from utils.validators import validate_request

create_site_bp = Blueprint('create_site', __name__)


@create_site_bp.route('/api/sites', methods=['POST'])
@validate_request(CreateSiteRequestSchema)
def create_site(validated_data):
    """
    Create a new site.

    Request body:
        name: Site name
        domain: Site domain (must be unique)

    Returns:
        201: Site created successfully
        400: Validation error or duplicate domain
    """
    current_time = int(time.time())

    site = Site(
        id=0,
        name=validated_data['name'],
        domain=validated_data['domain'],
        frontend_url=validated_data['frontend_url'],
        email_from=validated_data['email_from'],
        email_from_name=validated_data['email_from_name'],
        created_at=current_time,
        updated_at=current_time
    )

    try:
        created_site = db_manager.create_site(site)
        schema = SiteResponseSchema()
        return jsonify(schema.dump(created_site)), 201
    except Exception as e:
        if 'duplicate' in str(e).lower() or 'unique' in str(e).lower():
            return jsonify({'error': 'Domain already exists'}), 400
        return jsonify({'error': str(e)}), 500
