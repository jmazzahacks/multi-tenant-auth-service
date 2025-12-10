#!/usr/bin/env python3
"""
Interactive script to resend verification email for a user.
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


def list_sites(api_url: str, api_key: str) -> list:
    """Fetch and display all sites"""
    try:
        response = requests.get(
            f"{api_url}/api/sites",
            headers={'X-API-Key': api_key}
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"\n✗ Error fetching sites (HTTP {response.status_code}):")
            print(response.json())
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Error: Could not connect to {api_url}")
        print("Is the auth service running?")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


def select_site(sites: list) -> dict:
    """Display sites and let user select one"""
    if not sites:
        print("\n✗ No sites available. Create a site first.")
        sys.exit(1)

    print("\nAvailable Sites:")
    print("=" * 60)
    for idx, site in enumerate(sites, 1):
        print(f"{idx}. {site['name']} ({site['domain']})")
        print(f"   ID: {site['id']}")
    print("=" * 60)

    while True:
        choice = input(f"\nSelect a site (1-{len(sites)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sites):
                return sites[idx]
            else:
                print(f"Please enter a number between 1 and {len(sites)}")
        except ValueError:
            print("Please enter a valid number")


def list_unverified_users(api_url: str, api_key: str, site_id: int) -> list:
    """Fetch users for a site and filter to unverified only"""
    try:
        response = requests.get(
            f"{api_url}/api/sites/{site_id}/users",
            headers={'X-API-Key': api_key}
        )

        if response.status_code == 200:
            users = response.json()
            unverified = [u for u in users if not u['is_verified']]
            return unverified
        else:
            print(f"\n✗ Error fetching users (HTTP {response.status_code}):")
            print(response.json())
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Error: Could not connect to {api_url}")
        print("Is the auth service running?")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


def select_user(users: list) -> dict:
    """Display users and let user select one"""
    if not users:
        print("\n✗ No unverified users found for this site.")
        sys.exit(0)

    print("\nUnverified Users:")
    print("=" * 60)
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user['email']}")
        print(f"   ID: {user['id']}, Role: {user['role']}")
    print("=" * 60)

    while True:
        choice = input(f"\nSelect a user (1-{len(users)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(users):
                return users[idx]
            else:
                print(f"Please enter a number between 1 and {len(users)}")
        except ValueError:
            print("Please enter a valid number")


def main():
    print("=" * 60)
    print("Resend Verification Email - Multi-Tenant Auth Service")
    print("=" * 60)
    print()

    # Get API configuration
    api_url = get_input("Auth service URL", "http://127.0.0.1:5678")
    api_key = os.getenv('MASTER_API_KEY')

    if not api_key:
        api_key = get_input("Master API Key (or set MASTER_API_KEY in .env)")

    # Fetch and select site
    sites = list_sites(api_url, api_key)
    selected_site = select_site(sites)

    print(f"\nSelected site: {selected_site['name']} (ID: {selected_site['id']})")
    print("-" * 60)

    # Fetch unverified users for the site
    print("\nFetching unverified users...")
    unverified_users = list_unverified_users(api_url, api_key, selected_site['id'])
    selected_user = select_user(unverified_users)

    print()
    print("-" * 60)
    print(f"User: {selected_user['email']}")
    print(f"Site: {selected_site['name']}")
    print("-" * 60)

    # Confirm
    confirm = input("\nResend verification email? (y/n): ").strip().lower()
    if confirm not in ('y', 'yes'):
        print("Cancelled.")
        sys.exit(0)

    # Make API request
    print("\nSending verification email...")
    try:
        response = requests.post(
            f"{api_url}/api/admin/resend-verification/{selected_user['id']}",
            headers={'X-API-Key': api_key}
        )

        if response.status_code == 200:
            print("\n✓ Verification email sent successfully!")
            print(f"Check {selected_user['email']} for the verification link.")
        else:
            print(f"\n✗ Error (HTTP {response.status_code}):")
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
