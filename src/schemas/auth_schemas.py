"""
Marshmallow schemas for authentication API requests and responses.
"""
from marshmallow import Schema, fields, validate


class RegisterRequestSchema(Schema):
    """Schema for user registration request"""
    site_id = fields.Integer(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))


class LoginRequestSchema(Schema):
    """Schema for login request"""
    site_id = fields.Integer(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


class VerifyEmailRequestSchema(Schema):
    """Schema for email verification request"""
    token = fields.String(required=True)


class ChangePasswordRequestSchema(Schema):
    """Schema for password change request"""
    old_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=8))


class RequestPasswordResetSchema(Schema):
    """Schema for password reset request"""
    site_id = fields.Integer(required=True)
    email = fields.Email(required=True)


class ResetPasswordRequestSchema(Schema):
    """Schema for password reset with token"""
    token = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=8))


class RequestEmailChangeSchema(Schema):
    """Schema for email change request"""
    new_email = fields.Email(required=True)


class ConfirmEmailChangeSchema(Schema):
    """Schema for confirming email change"""
    token = fields.String(required=True)


class UserResponseSchema(Schema):
    """Schema for user response (no sensitive data)"""
    id = fields.Integer()
    site_id = fields.Integer()
    email = fields.Email()
    is_verified = fields.Boolean()
    role = fields.Method("get_role")
    created_at = fields.Integer()
    updated_at = fields.Integer()

    def get_role(self, obj):
        """Extract role value from UserRole enum"""
        return obj.role.value if hasattr(obj.role, 'value') else obj.role


class AuthTokenResponseSchema(Schema):
    """Schema for auth token response"""
    token = fields.String()
    user_id = fields.Integer()
    expires_at = fields.Integer()
