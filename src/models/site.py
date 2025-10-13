from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Site:
    """
    Site model representing a registered website/application (tenant).

    Each site is a separate tenant in the multi-tenant architecture.
    Users are scoped to a specific site.

    Attributes:
        id: Unique site identifier
        name: Human-readable name of the site
        domain: Domain name of the site (unique)
        frontend_url: Frontend URL for this site (used in email links)
        email_from: Email address to send emails from for this site
        email_from_name: Display name for emails sent from this site
        created_at: Unix timestamp when the site was created
        updated_at: Unix timestamp when the site was last updated
    """
    id: int
    name: str
    domain: str
    frontend_url: str
    email_from: str
    email_from_name: str
    created_at: int
    updated_at: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert site model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'frontend_url': self.frontend_url,
            'email_from': self.email_from,
            'email_from_name': self.email_from_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Site':
        """Create site model from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            domain=data['domain'],
            frontend_url=data['frontend_url'],
            email_from=data['email_from'],
            email_from_name=data['email_from_name'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
