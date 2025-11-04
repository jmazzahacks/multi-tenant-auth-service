#!/usr/bin/env python3
"""
Test the email_service integration with Mailgun.
Usage: python test-email-service.py <to_email>
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.email_service import email_service
from database import db_manager


def main():
    if len(sys.argv) < 2:
        print("Usage: python test-email-service.py <to_email>")
        sys.exit(1)

    test_email = sys.argv[1]

    print("=" * 60)
    print("Email Service Integration Test")
    print("=" * 60)

    # Get a site to test with
    with db_manager.get_cursor() as cursor:
        cursor.execute("SELECT id, name, frontend_url, email_from, email_from_name FROM sites LIMIT 1")
        site = cursor.fetchone()

    if not site:
        print("\n✗ No sites found. Create a site first.")
        sys.exit(1)

    print(f"\nUsing site: {site['name']}")
    print(f"From: {site['email_from_name']} <{site['email_from']}>")
    print(f"To: {test_email}")
    print("-" * 60)

    print(f"\nSending test verification email...")

    # Try to send email using email_service
    success = email_service.send_verification_email(
        to_email=test_email,
        token="test-token-12345",
        site_name=site['name'],
        frontend_url=site['frontend_url'],
        from_email=site['email_from'],
        from_name=site['email_from_name']
    )

    if success:
        print("\n✓ Email sent successfully!")
        print(f"Check {test_email} for the verification email.")
    else:
        print("\n✗ Email failed to send.")
        print("Check the logs above for error details.")
        sys.exit(1)


if __name__ == '__main__':
    main()
