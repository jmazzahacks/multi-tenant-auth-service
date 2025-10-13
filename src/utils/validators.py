"""
Utility functions for request validation using marshmallow schemas.
"""
from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError


def validate_request(schema_class):
    """
    Decorator to validate request JSON data using a marshmallow schema.

    Args:
        schema_class: The marshmallow schema class to use for validation

    Returns:
        Decorator function that validates request and passes validated data to the route
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            try:
                validated_data = schema.load(request.get_json() or {})
                return func(validated_data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({'error': 'Validation error', 'details': err.messages}), 400
        return wrapper
    return decorator
