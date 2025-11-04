#!/usr/bin/env python3
"""
Simple Mailgun test script based on official example.
Usage: python test-mailgun-simple.py <to_email>
"""
import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_test_message(to_email: str):
    """Send a simple test email via Mailgun"""

    # Load Mailgun credentials from environment
    api_key = os.getenv('MAILGUN_API_KEY')
    domain = os.getenv('MAILGUN_DOMAIN', 'podcastguru.io')

    if not api_key:
        print("✗ Error: MAILGUN_API_KEY not found in environment")
        print("Make sure .env file contains MAILGUN_API_KEY")
        sys.exit(1)

    print("=" * 60)
    print("Mailgun Simple Test")
    print("=" * 60)
    print(f"\nAPI Key: {api_key[:20]}...")
    print(f"Domain: {domain}")
    print(f"To: {to_email}")
    print("-" * 60)

    url = f"https://api.mailgun.net/v3/{domain}/messages"

    response = requests.post(
        url,
        auth=("api", api_key),
        data={
            "from": "PodcastGuru Support <support@podcastguru.io>",
            "to": to_email,
            "subject": "Hello from Mailgun",
            "text": "Congratulations! You just sent an email with Mailgun via the auth-service!"
        }
    )

    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {response.text}")

    if response.status_code == 200:
        print("\n✓ Email sent successfully!")
        return True
    else:
        print("\n✗ Email failed to send.")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test-mailgun-simple.py <to_email>")
        sys.exit(1)

    to_email = sys.argv[1]
    success = send_test_message(to_email)
    sys.exit(0 if success else 1)
