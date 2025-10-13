"""
Email service for sending transactional emails using SendGrid.
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from config import get_config
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SendGrid"""

    def __init__(self):
        """Initialize the email service with SendGrid API key from config"""
        config = get_config()
        self.api_key = config.SENDGRID_API_KEY

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        from_email: str,
        from_name: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email using SendGrid.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            from_email: Sender email address (site-specific)
            from_name: Sender display name (site-specific)
            text_content: Plain text content (optional)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.api_key:
            logger.error("SendGrid API key not configured")
            return False

        try:
            message = Mail(
                from_email=Email(from_email, from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )

            if text_content:
                message.plain_text_content = Content("text/plain", text_content)

            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)

            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

    def send_verification_email(
        self,
        to_email: str,
        token: str,
        site_name: str,
        frontend_url: str,
        from_email: str,
        from_name: str
    ) -> bool:
        """
        Send email verification email.

        Args:
            to_email: User's email address
            token: Verification token
            site_name: Name of the site
            frontend_url: Frontend URL for this site
            from_email: Sender email address (site-specific)
            from_name: Sender display name (site-specific)

        Returns:
            bool: True if sent successfully
        """
        verification_url = f"{frontend_url}/verify-email?token={token}"

        subject = f"Verify your email for {site_name}"

        html_content = f"""
        <html>
            <body>
                <h2>Welcome to {site_name}!</h2>
                <p>Please verify your email address by clicking the link below:</p>
                <p><a href="{verification_url}">Verify Email</a></p>
                <p>Or copy and paste this URL into your browser:</p>
                <p>{verification_url}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't create an account, you can safely ignore this email.</p>
            </body>
        </html>
        """

        text_content = f"""
        Welcome to {site_name}!

        Please verify your email address by visiting this URL:
        {verification_url}

        This link will expire in 24 hours.

        If you didn't create an account, you can safely ignore this email.
        """

        return self.send_email(to_email, subject, html_content, from_email, from_name, text_content)

    def send_password_reset_email(
        self,
        to_email: str,
        token: str,
        site_name: str,
        frontend_url: str,
        from_email: str,
        from_name: str
    ) -> bool:
        """
        Send password reset email.

        Args:
            to_email: User's email address
            token: Password reset token
            site_name: Name of the site
            frontend_url: Frontend URL for this site
            from_email: Sender email address (site-specific)
            from_name: Sender display name (site-specific)

        Returns:
            bool: True if sent successfully
        """
        reset_url = f"{frontend_url}/reset-password?token={token}"

        subject = f"Reset your password for {site_name}"

        html_content = f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>We received a request to reset your password for {site_name}.</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="{reset_url}">Reset Password</a></p>
                <p>Or copy and paste this URL into your browser:</p>
                <p>{reset_url}</p>
                <p>This link will expire in 1 hour.</p>
                <p>If you didn't request a password reset, you can safely ignore this email.</p>
            </body>
        </html>
        """

        text_content = f"""
        Password Reset Request

        We received a request to reset your password for {site_name}.

        Visit this URL to reset your password:
        {reset_url}

        This link will expire in 1 hour.

        If you didn't request a password reset, you can safely ignore this email.
        """

        return self.send_email(to_email, subject, html_content, from_email, from_name, text_content)

    def send_email_change_confirmation(
        self,
        to_email: str,
        token: str,
        site_name: str,
        frontend_url: str,
        from_email: str,
        from_name: str
    ) -> bool:
        """
        Send email change confirmation email.

        Args:
            to_email: New email address
            token: Email change confirmation token
            site_name: Name of the site
            frontend_url: Frontend URL for this site
            from_email: Sender email address (site-specific)
            from_name: Sender display name (site-specific)

        Returns:
            bool: True if sent successfully
        """
        confirmation_url = f"{frontend_url}/confirm-email-change?token={token}"

        subject = f"Confirm your email change for {site_name}"

        html_content = f"""
        <html>
            <body>
                <h2>Email Change Confirmation</h2>
                <p>You requested to change your email address for {site_name}.</p>
                <p>Click the link below to confirm this change:</p>
                <p><a href="{confirmation_url}">Confirm Email Change</a></p>
                <p>Or copy and paste this URL into your browser:</p>
                <p>{confirmation_url}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't request this change, please ignore this email and contact support immediately.</p>
            </body>
        </html>
        """

        text_content = f"""
        Email Change Confirmation

        You requested to change your email address for {site_name}.

        Visit this URL to confirm this change:
        {confirmation_url}

        This link will expire in 24 hours.

        If you didn't request this change, please ignore this email and contact support immediately.
        """

        return self.send_email(to_email, subject, html_content, from_email, from_name, text_content)


# Singleton instance
email_service = EmailService()
