import bcrypt


class PasswordService:
    """Service for password hashing and verification using bcrypt"""

    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password using bcrypt.

        Args:
            password: The plain text password to hash

        Returns:
            str: The bcrypt hashed password as a string
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a plain text password against a bcrypt hash.

        Args:
            password: The plain text password to verify
            password_hash: The bcrypt hash to compare against

        Returns:
            bool: True if password matches hash, False otherwise
        """
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)


# Global password service instance
password_service = PasswordService()
