"""
Get site endpoint.
"""
from flask import Blueprint, jsonify, request
from database import db_manager
from schemas.site_schemas import SiteResponseSchema

get_site_bp = Blueprint('get_site', __name__)


@get_site_bp.route('/api/sites/by-domain', methods=['GET'])
def get_site_by_domain():
    """
    Get a site by domain.

    Query parameters:
        domain: Site domain

    Returns:
        200: Site found
        400: Missing domain parameter
        404: Site not found
    """
    domain = request.args.get('domain')

    if not domain:
        return jsonify({'error': 'Domain parameter is required'}), 400

    site = db_manager.find_site_by_domain(domain)

    if site is None:
        return jsonify({'error': 'Site not found'}), 404

    schema = SiteResponseSchema()
    return jsonify(schema.dump(site)), 200


@get_site_bp.route('/api/sites/<int:site_id>', methods=['GET'])
def get_site_by_id(site_id):
    """
    Get a site by ID.

    Path parameters:
        site_id: Site ID

    Returns:
        200: Site found
        404: Site not found
    """
    site = db_manager.find_site_by_id(site_id)

    if site is None:
        return jsonify({'error': 'Site not found'}), 404

    schema = SiteResponseSchema()
    return jsonify(schema.dump(site)), 200
