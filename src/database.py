import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator, Optional
from config import get_config


class DatabaseManager:
    """Manages PostgreSQL database connections with connection pooling"""

    def __init__(self, min_conn: int = 1, max_conn: int = 10):
        self.config = get_config()
        self.connection_pool = None

        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                min_conn,
                max_conn,
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
            print("Database connection pool initialized successfully")
        except Exception as e:
            print(f"Error initializing database pool: {e}")
            raise

    def close_pool(self) -> None:
        """Close all connections in the pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
            print("Database connection pool closed")

    def __del__(self):
        """Cleanup connection pool when instance is destroyed"""
        self.close_pool()

    @contextmanager
    def get_connection(self) -> Generator:
        """Context manager for getting a database connection from the pool"""
        if not self.connection_pool:
            raise Exception("Connection pool not initialized")

        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)

    @contextmanager
    def get_cursor(self, commit: bool = False) -> Generator:
        """Context manager for getting a cursor with automatic commit/rollback"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                if commit:
                    conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()

    # Site operations
    def create_site(self, site: 'Site') -> 'Site':
        """
        Create a new site in the database.

        Args:
            site: Site model with name, domain, frontend_url, email_from, email_from_name, created_at, updated_at

        Returns:
            Site: The created site with auto-generated id
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO sites (name, domain, frontend_url, email_from, email_from_name, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (site.name, site.domain, site.frontend_url, site.email_from, site.email_from_name, site.created_at, site.updated_at)
            )
            site.id = cursor.fetchone()['id']
        return site

    def find_site_by_id(self, site_id: int) -> Optional['Site']:
        """
        Find a site by its ID.

        Args:
            site_id: The site's ID

        Returns:
            Optional[Site]: The site if found, None otherwise
        """
        from models.site import Site

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, name, domain, frontend_url, email_from, email_from_name, created_at, updated_at FROM sites WHERE id = %s",
                (site_id,)
            )
            row = cursor.fetchone()
            return Site.from_dict(row) if row else None

    def find_site_by_domain(self, domain: str) -> Optional['Site']:
        """
        Find a site by its domain.

        Args:
            domain: The site's domain

        Returns:
            Optional[Site]: The site if found, None otherwise
        """
        from models.site import Site

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, name, domain, frontend_url, email_from, email_from_name, created_at, updated_at FROM sites WHERE domain = %s",
                (domain,)
            )
            row = cursor.fetchone()
            return Site.from_dict(row) if row else None

    def update_site(self, site: 'Site') -> 'Site':
        """
        Update an existing site in the database.

        Args:
            site: Site model with all fields including id

        Returns:
            Site: The updated site model
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE sites
                SET name = %s, domain = %s, frontend_url = %s, email_from = %s, email_from_name = %s, updated_at = %s
                WHERE id = %s
                """,
                (site.name, site.domain, site.frontend_url, site.email_from, site.email_from_name, site.updated_at, site.id)
            )
        return site

    # User operations
    def create_user(self, user: 'User') -> 'User':
        """
        Create a new user in the database.

        Args:
            user: User model with site_id, email, password_hash, is_verified, role, created_at, updated_at

        Returns:
            User: The created user with auto-generated id
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO users (site_id, email, password_hash, is_verified, role, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (user.site_id, user.email, user.password_hash, user.is_verified, user.role.value, user.created_at, user.updated_at)
            )
            user.id = cursor.fetchone()['id']
        return user

    def find_user_by_id(self, user_id: int) -> Optional['User']:
        """
        Find a user by their ID.

        Args:
            user_id: The user's ID

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        from models.user import User

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, site_id, email, password_hash, is_verified, role, created_at, updated_at FROM users WHERE id = %s",
                (user_id,)
            )
            row = cursor.fetchone()
            return User.from_dict(row) if row else None

    def find_user_by_email(self, site_id: int, email: str) -> Optional['User']:
        """
        Find a user by their email address within a specific site.

        Args:
            site_id: The site ID to search within
            email: The user's email address

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        from models.user import User

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, site_id, email, password_hash, is_verified, role, created_at, updated_at FROM users WHERE site_id = %s AND email = %s",
                (site_id, email)
            )
            row = cursor.fetchone()
            return User.from_dict(row) if row else None

    def update_user(self, user: 'User') -> 'User':
        """
        Update an existing user in the database.

        Args:
            user: User model with all fields including id

        Returns:
            User: The updated user model
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE users
                SET email = %s, password_hash = %s, is_verified = %s, role = %s, updated_at = %s
                WHERE id = %s
                """,
                (user.email, user.password_hash, user.is_verified, user.role.value, user.updated_at, user.id)
            )
        return user

    # AuthToken operations
    def create_auth_token(self, auth_token: 'AuthToken') -> 'AuthToken':
        """
        Create a new auth token in the database.

        Args:
            auth_token: AuthToken model with all fields

        Returns:
            AuthToken: The created auth token
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO auth_tokens (site_id, user_id, token, expires_at, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (auth_token.site_id, auth_token.user_id, auth_token.token, auth_token.expires_at, auth_token.created_at)
            )
        return auth_token

    def find_auth_token_by_token(self, token: str) -> Optional['AuthToken']:
        """
        Find an auth token by its token string.

        Args:
            token: The token string to search for

        Returns:
            Optional[AuthToken]: The auth token if found, None otherwise
        """
        from models.auth_token import AuthToken

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT site_id, user_id, token, expires_at, created_at FROM auth_tokens WHERE token = %s",
                (token,)
            )
            row = cursor.fetchone()
            return AuthToken.from_dict(row) if row else None

    def delete_auth_token(self, token: str) -> bool:
        """
        Delete an auth token by its token string.

        Args:
            token: The token string to delete

        Returns:
            bool: True if token was deleted, False if not found
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM auth_tokens WHERE token = %s", (token,))
            return cursor.rowcount > 0

    def delete_auth_tokens_by_user(self, user_id: int) -> int:
        """
        Delete all auth tokens for a user.

        Args:
            user_id: The user's ID

        Returns:
            int: Number of tokens deleted
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM auth_tokens WHERE user_id = %s", (user_id,))
            return cursor.rowcount

    def delete_expired_auth_tokens(self, current_time: int) -> int:
        """
        Delete all expired auth tokens.

        Args:
            current_time: Unix timestamp to compare against

        Returns:
            int: Number of tokens deleted
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM auth_tokens WHERE expires_at < %s", (current_time,))
            return cursor.rowcount

    # EmailVerificationToken operations
    def create_email_verification_token(self, token: 'EmailVerificationToken') -> 'EmailVerificationToken':
        """
        Create a new email verification token in the database.

        Args:
            token: EmailVerificationToken model with all fields

        Returns:
            EmailVerificationToken: The created token
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO email_verification_tokens (site_id, user_id, token, expires_at, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (token.site_id, token.user_id, token.token, token.expires_at, token.created_at)
            )
        return token

    def find_email_verification_token(self, token: str) -> Optional['EmailVerificationToken']:
        """
        Find an email verification token by its token string.

        Args:
            token: The token string to search for

        Returns:
            Optional[EmailVerificationToken]: The token if found, None otherwise
        """
        from models.email_verification_token import EmailVerificationToken

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT site_id, user_id, token, expires_at, created_at FROM email_verification_tokens WHERE token = %s",
                (token,)
            )
            row = cursor.fetchone()
            return EmailVerificationToken.from_dict(row) if row else None

    def delete_email_verification_token(self, token: str) -> bool:
        """
        Delete an email verification token.

        Args:
            token: The token string to delete

        Returns:
            bool: True if deleted, False if not found
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM email_verification_tokens WHERE token = %s", (token,))
            return cursor.rowcount > 0

    def delete_expired_email_verification_tokens(self, current_time: int) -> int:
        """
        Delete all expired email verification tokens.

        Args:
            current_time: Unix timestamp to compare against

        Returns:
            int: Number of tokens deleted
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM email_verification_tokens WHERE expires_at < %s", (current_time,))
            return cursor.rowcount

    # PasswordResetToken operations
    def create_password_reset_token(self, token: 'PasswordResetToken') -> 'PasswordResetToken':
        """
        Create a new password reset token in the database.

        Args:
            token: PasswordResetToken model with all fields

        Returns:
            PasswordResetToken: The created token
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO password_reset_tokens (site_id, user_id, token, expires_at, created_at, used)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (token.site_id, token.user_id, token.token, token.expires_at, token.created_at, token.used)
            )
        return token

    def find_password_reset_token(self, token: str) -> Optional['PasswordResetToken']:
        """
        Find a password reset token by its token string.

        Args:
            token: The token string to search for

        Returns:
            Optional[PasswordResetToken]: The token if found, None otherwise
        """
        from models.password_reset_token import PasswordResetToken

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT site_id, user_id, token, expires_at, created_at, used FROM password_reset_tokens WHERE token = %s",
                (token,)
            )
            row = cursor.fetchone()
            return PasswordResetToken.from_dict(row) if row else None

    def mark_password_reset_token_used(self, token: str) -> bool:
        """
        Mark a password reset token as used.

        Args:
            token: The token string to mark as used

        Returns:
            bool: True if updated, False if not found
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("UPDATE password_reset_tokens SET used = TRUE WHERE token = %s", (token,))
            return cursor.rowcount > 0

    def delete_expired_password_reset_tokens(self, current_time: int) -> int:
        """
        Delete all expired password reset tokens.

        Args:
            current_time: Unix timestamp to compare against

        Returns:
            int: Number of tokens deleted
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM password_reset_tokens WHERE expires_at < %s", (current_time,))
            return cursor.rowcount

    # EmailChangeRequest operations
    def create_email_change_request(self, request: 'EmailChangeRequest') -> 'EmailChangeRequest':
        """
        Create a new email change request in the database.

        Args:
            request: EmailChangeRequest model with all fields

        Returns:
            EmailChangeRequest: The created request
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO email_change_requests (site_id, user_id, new_email, token, expires_at, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (request.site_id, request.user_id, request.new_email, request.token, request.expires_at, request.created_at)
            )
        return request

    def find_email_change_request(self, token: str) -> Optional['EmailChangeRequest']:
        """
        Find an email change request by its token string.

        Args:
            token: The token string to search for

        Returns:
            Optional[EmailChangeRequest]: The request if found, None otherwise
        """
        from models.email_change_request import EmailChangeRequest

        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT site_id, user_id, new_email, token, expires_at, created_at FROM email_change_requests WHERE token = %s",
                (token,)
            )
            row = cursor.fetchone()
            return EmailChangeRequest.from_dict(row) if row else None

    def delete_email_change_request(self, token: str) -> bool:
        """
        Delete an email change request.

        Args:
            token: The token string to delete

        Returns:
            bool: True if deleted, False if not found
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM email_change_requests WHERE token = %s", (token,))
            return cursor.rowcount > 0

    def delete_expired_email_change_requests(self, current_time: int) -> int:
        """
        Delete all expired email change requests.

        Args:
            current_time: Unix timestamp to compare against

        Returns:
            int: Number of requests deleted
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM email_change_requests WHERE expires_at < %s", (current_time,))
            return cursor.rowcount


# Global database manager instance
db_manager = DatabaseManager()
