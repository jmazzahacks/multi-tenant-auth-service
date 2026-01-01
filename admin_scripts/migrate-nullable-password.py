#!/usr/bin/env python
"""
One-off migration script to make password_hash column nullable.

This allows admin-created users to be created without a password,
setting their password later during email verification.

Usage:
    source bin/activate && python admin_scripts/migrate-nullable-password.py
"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_db_config() -> dict:
    """Get database configuration from environment"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'aegis'),
        'user': os.getenv('DB_USER', 'aegis_admin'),
        'password': os.getenv('DB_PASSWORD', 'aegis_admin')
    }


def check_column_nullable(cursor) -> bool:
    """Check if password_hash column is already nullable"""
    cursor.execute("""
        SELECT is_nullable
        FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'password_hash'
    """)
    result = cursor.fetchone()
    if result:
        return result[0] == 'YES'
    return False


def main():
    print("=" * 60)
    print("Migration: Make password_hash nullable")
    print("=" * 60)
    print()

    config = get_db_config()
    print(f"Database: {config['database']}@{config['host']}:{config['port']}")
    print()

    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # Check current state
        if check_column_nullable(cursor):
            print("Column 'password_hash' is already nullable.")
            print("Migration not needed - already applied.")
            cursor.close()
            conn.close()
            return

        print("Current state: password_hash is NOT NULL")
        print()

        # Confirm
        confirm = input("Apply migration to make password_hash nullable? (y/n): ").strip().lower()
        if confirm not in ('y', 'yes'):
            print("Cancelled.")
            cursor.close()
            conn.close()
            sys.exit(0)

        print()
        print("Applying migration...")

        # Run migration
        cursor.execute("""
            ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL
        """)
        conn.commit()

        # Verify
        if check_column_nullable(cursor):
            print()
            print("=" * 60)
            print("Migration completed successfully!")
            print("Column 'password_hash' is now nullable.")
            print("=" * 60)
        else:
            print()
            print("ERROR: Migration may have failed. Please verify manually.")
            sys.exit(1)

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"\nDatabase error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
