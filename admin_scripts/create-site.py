#!/usr/bin/env python3
"""
Interactive script to create a new site in the auth service.
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_input(prompt: str, default: str = None) -> str:
    """Get user input with optional default value"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("This field is required. Please try again.")


def main():
    print("=" * 60)
    print("Create New Site - Multi-Tenant Auth Service")
    print("=" * 60)
    print()

    # Get API configuration
    api_url = get_input("Auth service URL", "http://127.0.0.1:5678")
    api_key = os.getenv('MASTER_API_KEY')

    if not api_key:
        api_key = get_input("Master API Key (or set MASTER_API_KEY in .env)")

    print()
    print("Enter site details:")
    print("-" * 60)

    # Collect site information
    site_data = {
        'name': get_input("Site name (e.g., 'My Website')"),
        'domain': get_input("Domain (e.g., 'example.com')"),
        'frontend_url': get_input("Frontend URL (e.g., 'https://example.com')"),
        'email_from': get_input("Email from address (e.g., 'noreply@example.com')"),
        'email_from_name': get_input("Email from name (e.g., 'My Website')")
    }

    print()
    print("-" * 60)
    print("Site details to create:")
    print("-" * 60)
    for key, value in site_data.items():
        print(f"  {key}: {value}")
    print("-" * 60)

    # Confirm
    confirm = input("\nCreate this site? (y/n): ").strip().lower()
    if confirm not in ('y', 'yes'):
        print("Cancelled.")
        sys.exit(0)

    # Make API request
    print("\nCreating site...")
    try:
        response = requests.post(
            f"{api_url}/api/sites",
            headers={
                'X-API-Key': api_key,
                'Content-Type': 'application/json'
            },
            json=site_data
        )

        if response.status_code == 201:
            site = response.json()
            print("\n✓ Site created successfully!")
            print("=" * 60)
            print(f"Site ID: {site['id']}")
            print(f"Name: {site['name']}")
            print(f"Domain: {site['domain']}")
            print(f"Frontend URL: {site['frontend_url']}")
            print(f"Email From: {site['email_from_name']} <{site['email_from']}>")
            print(f"Created: {site['created_at']}")
            print("=" * 60)
            print(f"\nUse site_id={site['id']} in your frontend configuration.")
        else:
            print(f"\n✗ Error creating site (HTTP {response.status_code}):")
            print(response.json())
            sys.exit(1)

    except requests.exceptions.ConnectionError:
        print(f"\n✗ Error: Could not connect to {api_url}")
        print("Is the auth service running?")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
