#!/usr/bin/env python3
"""
Script to list all users for a site in the auth service.
Requires either --site-id or --domain parameter.
"""
import argparse
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_input(prompt: str) -> str:
    """Get user input"""
    while True:
        user_input = input(f"{prompt}: ").strip()
        if user_input:
            return user_input
        print("This field is required. Please try again.")


def main():
    parser = argparse.ArgumentParser(
        description='List all users for a site in the auth service'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--site-id', type=int, help='Site ID')
    group.add_argument('--domain', type=str, help='Site domain')

    args = parser.parse_args()

    print("=" * 70)
    print("List Users - Multi-Tenant Auth Service")
    print("=" * 70)
    print()

    # Get API configuration
    api_url = os.getenv('API_URL', 'http://127.0.0.1:5678')
    api_key = os.getenv('MASTER_API_KEY')

    if not api_key:
        api_key = get_input("Master API Key (or set MASTER_API_KEY in .env)")

    # Build the appropriate URL
    if args.site_id:
        url = f"{api_url}/api/sites/{args.site_id}/users"
        identifier = f"site_id={args.site_id}"
    else:
        url = f"{api_url}/api/sites/by-domain/users?domain={args.domain}"
        identifier = f"domain={args.domain}"

    # Make API request
    print(f"Fetching users for {identifier}...")
    try:
        response = requests.get(
            url,
            headers={
                'X-API-Key': api_key,
                'Content-Type': 'application/json'
            }
        )

        if response.status_code == 200:
            users = response.json()

            if not users:
                print(f"\nNo users found for {identifier}.")
                return

            print(f"\nFound {len(users)} user(s):")
            print("=" * 70)

            for user in users:
                verified_status = "verified" if user['is_verified'] else "not verified"
                print(f"\nID: {user['id']}")
                print(f"  Email:    {user['email']}")
                print(f"  Role:     {user['role']}")
                print(f"  Status:   {verified_status}")
                print(f"  Created:  {user['created_at']}")

            print()
            print("=" * 70)
        elif response.status_code == 404:
            print(f"\n✗ Site not found for {identifier}")
            sys.exit(1)
        else:
            print(f"\n✗ Error listing users (HTTP {response.status_code}):")
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
