"""
Marshmallow schemas for site API requests and responses.
"""
from marshmallow import Schema, fields, validate


class CreateSiteRequestSchema(Schema):
    """Schema for creating a new site"""
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    domain = fields.String(required=True, validate=validate.Length(min=1, max=255))
    frontend_url = fields.Url(required=True)
    email_from = fields.Email(required=True)
    email_from_name = fields.String(required=True, validate=validate.Length(min=1, max=255))


class SiteResponseSchema(Schema):
    """Schema for site response"""
    id = fields.Integer()
    name = fields.String()
    domain = fields.String()
    frontend_url = fields.Url()
    email_from = fields.Email()
    email_from_name = fields.String()
    created_at = fields.Integer()
    updated_at = fields.Integer()
