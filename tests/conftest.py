import pytest
import time
import os
import sys

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import db_manager
from models.site import Site
from models.user import User


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """Set environment to use test database"""
    os.environ['DB_NAME'] = 'auth_service_test'
    yield


@pytest.fixture(scope='function')
def clean_database():
    """Clean all tables before each test"""
    with db_manager.get_cursor(commit=True) as cursor:
        cursor.execute("TRUNCATE sites, users, auth_tokens, email_verification_tokens, password_reset_tokens, email_change_requests CASCADE")
    yield
    with db_manager.get_cursor(commit=True) as cursor:
        cursor.execute("TRUNCATE sites, users, auth_tokens, email_verification_tokens, password_reset_tokens, email_change_requests CASCADE")


@pytest.fixture
def sample_site(clean_database):
    """Create a sample site for testing"""
    current_time = int(time.time())
    site = Site(
        id=0,
        name="Test Site",
        domain="test.example.com",
        frontend_url="http://test.example.com",
        email_from="noreply@test.example.com",
        email_from_name="Test Site",
        created_at=current_time,
        updated_at=current_time
    )
    return db_manager.create_site(site)


@pytest.fixture
def sample_user(sample_site):
    """Create a sample user for testing"""
    current_time = int(time.time())
    user = User(
        id=0,
        site_id=sample_site.id,
        email="test@example.com",
        password_hash="$2b$12$hashed_password",
        is_verified=False,
        created_at=current_time,
        updated_at=current_time
    )
    return db_manager.create_user(user)
