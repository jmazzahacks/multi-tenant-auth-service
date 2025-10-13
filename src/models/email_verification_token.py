from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EmailVerificationToken:
    """
    Email verification token model for confirming user email ownership.

    Sent to users upon registration to verify their email address.
    One-time use token that is deleted upon successful verification.
    Scoped to a specific site.

    Attributes:
        token: Unique secure token string
        site_id: ID of the site this token belongs to
        user_id: ID of the user this token belongs to
        expires_at: Unix timestamp when the token expires
        created_at: Unix timestamp when the token was created
    """
    token: str
    site_id: int
    user_id: int
    expires_at: int
    created_at: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert email verification token model to dictionary"""
        return {
            'token': self.token,
            'site_id': self.site_id,
            'user_id': self.user_id,
            'expires_at': self.expires_at,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmailVerificationToken':
        """Create email verification token model from dictionary"""
        return cls(
            token=data['token'],
            site_id=data['site_id'],
            user_id=data['user_id'],
            expires_at=data['expires_at'],
            created_at=data['created_at']
        )
