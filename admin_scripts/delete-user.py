#!/usr/bin/env python
"""
Interactive script to delete a user from the auth service.
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


def list_users(api_url: str, api_key: str, site_id: int) -> list:
    """Fetch all users for a site"""
    try:
        response = requests.get(
            f"{api_url}/api/sites/{site_id}/users",
            headers={'X-API-Key': api_key}
        )

        if response.status_code == 200:
            return response.json()
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
        print("\n✗ No users found for this site.")
        sys.exit(0)

    print("\nUsers:")
    print("=" * 60)
    for idx, user in enumerate(users, 1):
        verified_status = "verified" if user['is_verified'] else "unverified"
        print(f"{idx}. {user['email']}")
        print(f"   ID: {user['id']}, Role: {user['role']}, Status: {verified_status}")
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
    print("Delete User - Multi-Tenant Auth Service")
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

    # Fetch users for the site
    print("\nFetching users...")
    users = list_users(api_url, api_key, selected_site['id'])
    selected_user = select_user(users)

    print()
    print("-" * 60)
    print("WARNING: This action cannot be undone!")
    print("-" * 60)
    print(f"User ID:    {selected_user['id']}")
    print(f"Email:      {selected_user['email']}")
    print(f"Role:       {selected_user['role']}")
    print(f"Verified:   {selected_user['is_verified']}")
    print(f"Site:       {selected_site['name']}")
    print("-" * 60)

    # Double confirmation for destructive action
    confirm = input("\nAre you sure you want to delete this user? (y/n): ").strip().lower()
    if confirm not in ('y', 'yes'):
        print("Cancelled.")
        sys.exit(0)

    confirm_email = input(f"Type the user's email to confirm ({selected_user['email']}): ").strip()
    if confirm_email != selected_user['email']:
        print("Email does not match. Cancelled.")
        sys.exit(0)

    # Make API request
    print("\nDeleting user...")
    try:
        response = requests.delete(
            f"{api_url}/api/admin/users/{selected_user['id']}",
            headers={'X-API-Key': api_key}
        )

        if response.status_code == 200:
            print(f"\n✓ User {selected_user['email']} deleted successfully!")
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
