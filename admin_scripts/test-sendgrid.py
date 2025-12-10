#!/usr/bin/env python3
"""
Test SendGrid email sending to debug email issues.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.email_service import email_service
from database import db_manager


def main():
    print("=" * 60)
    print("SendGrid Email Test")
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
    print("-" * 60)

    # Get test email
    test_email = input("\nEnter email address to send test to: ").strip()
    if not test_email:
        print("Cancelled.")
        sys.exit(0)

    print(f"\nSending test verification email to {test_email}...")
    print("(Check server logs for detailed errors)")

    # Try to send email
    success = email_service.send_verification_email(
        to_email=test_email,
        token="test-token-12345",
        site_name=site['name'],
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
