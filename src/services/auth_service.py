import time
import logging
from typing import Optional
from database import db_manager
from models.user import User
from models.user_role import UserRole
from models.auth_token import AuthToken
from services.password_service import password_service
from services.token_service import token_service
from services.email_service import email_service

logger = logging.getLogger(__name__)


class AuthService:
    """Service for user authentication and account management"""

    def register_user(self, site_id: int, email: str, password: str, role: UserRole = UserRole.USER) -> User:
        """
        Register a new user account for a specific site.

        Creates a new user with hashed password and generates an email
        verification token. The user is not verified by default.

        Args:
            site_id: The ID of the site to register the user for
            email: The user's email address
            password: The user's plain text password
            role: The user's role (defaults to USER)

        Returns:
            User: The created user model

        Raises:
            ValueError: If email already exists for this site
        """
        # Check if email already exists for this site
        existing_user = db_manager.find_user_by_email(site_id, email)
        if existing_user:
            raise ValueError("Email already registered for this site")

        # Hash password
        password_hash = password_service.hash_password(password)

        # Create user
        current_time = int(time.time())
        user = User(
            id=0,  # Will be set by database
            site_id=site_id,
            email=email,
            password_hash=password_hash,
            is_verified=False,
            role=role,
            created_at=current_time,
            updated_at=current_time
        )

        user = db_manager.create_user(user)

        # Create email verification token
        verification_token = token_service.create_email_verification_token(site_id, user.id)

        # Get site info for email
        site = db_manager.find_site_by_id(site_id)
        if site:
            # Send verification email (don't fail if email fails)
            try:
                email_service.send_verification_email(
                    to_email=user.email,
                    token=verification_token.token,
                    site_name=site.name,
                    frontend_url=site.frontend_url,
                    from_email=site.email_from,
                    from_name=site.email_from_name
                )
            except Exception as e:
                logger.error(f"Failed to send verification email: {str(e)}")

        return user

    def login(self, site_id: int, email: str, password: str) -> AuthToken:
        """
        Authenticate a user with email and password for a specific site.

        Args:
            site_id: The ID of the site to authenticate for
            email: The user's email address
            password: The user's plain text password

        Returns:
            AuthToken: The created auth token

        Raises:
            ValueError: If credentials are invalid or email not verified
        """
        # Find user by email for this site
        user = db_manager.find_user_by_email(site_id, email)
        if not user:
            raise ValueError("Invalid credentials")

        # Verify password
        if not password_service.verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        # Check if email is verified
        if not user.is_verified:
            raise ValueError("Email not verified")

        # Create auth token
        auth_token = token_service.create_auth_token(site_id, user.id)

        return auth_token

    def logout(self, token: str) -> bool:
        """
        Logout a user by invalidating their auth token.

        Args:
            token: The auth token to invalidate

        Returns:
            bool: True if token was invalidated, False if not found
        """
        return token_service.invalidate_auth_token(token)

    def verify_email(self, token: str) -> User:
        """
        Verify a user's email address using a verification token.

        Args:
            token: The email verification token

        Returns:
            User: The updated user with is_verified=True

        Raises:
            ValueError: If token is invalid or expired
        """
        user_id = token_service.validate_email_verification_token(token)
        if not user_id:
            raise ValueError("Invalid or expired verification token")

        # Update user verification status
        user = db_manager.find_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.is_verified = True
        user.updated_at = int(time.time())

        return db_manager.update_user(user)

    def change_password(self, user_id: int, old_password: str, new_password: str) -> User:
        """
        Change a user's password after verifying the old password.

        Args:
            user_id: The user's ID
            old_password: The user's current password
            new_password: The new password to set

        Returns:
            User: The updated user

        Raises:
            ValueError: If old password is incorrect or user not found
        """
        user = db_manager.find_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Verify old password
        if not password_service.verify_password(old_password, user.password_hash):
            raise ValueError("Incorrect password")

        # Hash new password
        user.password_hash = password_service.hash_password(new_password)
        user.updated_at = int(time.time())

        # Update user
        updated_user = db_manager.update_user(user)

        # Invalidate all existing auth tokens for security
        token_service.invalidate_user_tokens(user_id)

        return updated_user

    def request_password_reset(self, site_id: int, email: str) -> Optional[str]:
        """
        Request a password reset token for a user.

        Args:
            site_id: The ID of the site
            email: The user's email address

        Returns:
            Optional[str]: The reset token if user exists, None otherwise
        """
        user = db_manager.find_user_by_email(site_id, email)
        if not user:
            # Don't reveal if email exists or not for security
            return None

        reset_token = token_service.create_password_reset_token(site_id, user.id)

        # Get site info for email
        site = db_manager.find_site_by_id(site_id)
        if site:
            # Send password reset email (don't fail if email fails)
            try:
                email_service.send_password_reset_email(
                    to_email=user.email,
                    token=reset_token.token,
                    site_name=site.name,
                    frontend_url=site.frontend_url,
                    from_email=site.email_from,
                    from_name=site.email_from_name
                )
            except Exception as e:
                logger.error(f"Failed to send password reset email: {str(e)}")

        return reset_token.token

    def reset_password(self, token: str, new_password: str) -> User:
        """
        Reset a user's password using a password reset token.

        Args:
            token: The password reset token
            new_password: The new password to set

        Returns:
            User: The updated user

        Raises:
            ValueError: If token is invalid, expired, or already used
        """
        user_id = token_service.validate_password_reset_token(token)
        if not user_id:
            raise ValueError("Invalid or expired reset token")

        user = db_manager.find_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Hash new password
        user.password_hash = password_service.hash_password(new_password)
        user.updated_at = int(time.time())

        # Update user
        updated_user = db_manager.update_user(user)

        # Invalidate all existing auth tokens for security
        token_service.invalidate_user_tokens(user_id)

        return updated_user

    def request_email_change(self, user_id: int, new_email: str) -> str:
        """
        Request an email change for a user.

        Args:
            user_id: The user's ID
            new_email: The new email address to verify

        Returns:
            str: The email change token

        Raises:
            ValueError: If new email is already in use or user not found
        """
        user = db_manager.find_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Check if new email is already in use for this site
        existing_user = db_manager.find_user_by_email(user.site_id, new_email)
        if existing_user:
            raise ValueError("Email already in use")

        change_request = token_service.create_email_change_token(user.site_id, user_id, new_email)

        # Get site info for email
        site = db_manager.find_site_by_id(user.site_id)
        if site:
            # Send email change confirmation (don't fail if email fails)
            try:
                email_service.send_email_change_confirmation(
                    to_email=new_email,
                    token=change_request.token,
                    site_name=site.name,
                    frontend_url=site.frontend_url,
                    from_email=site.email_from,
                    from_name=site.email_from_name
                )
            except Exception as e:
                logger.error(f"Failed to send email change confirmation: {str(e)}")

        return change_request.token

    def confirm_email_change(self, token: str) -> User:
        """
        Confirm an email change using a verification token.

        Args:
            token: The email change token

        Returns:
            User: The updated user with new email

        Raises:
            ValueError: If token is invalid or expired
        """
        change_request = token_service.validate_email_change_token(token)
        if not change_request:
            raise ValueError("Invalid or expired email change token")

        user = db_manager.find_user_by_id(change_request.user_id)
        if not user:
            raise ValueError("User not found")

        # Update email
        user.email = change_request.new_email
        user.updated_at = int(time.time())

        return db_manager.update_user(user)

    def get_user_by_token(self, token: str) -> Optional[User]:
        """
        Get a user by their auth token.

        Args:
            token: The auth token

        Returns:
            Optional[User]: The user if token is valid, None otherwise
        """
        user_id = token_service.validate_auth_token(token)
        if not user_id:
            return None

        return db_manager.find_user_by_id(user_id)


# Global auth service instance
auth_service = AuthService()
