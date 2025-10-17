# Multi-Tenant Auth Service

Multi-tenant authentication API built with Flask and PostgreSQL. Supports user registration, login, email verification, password management, and role-based authorization for multiple sites.

## Features

- **Multi-tenant Architecture** - Isolate users and authentication by site/domain
- **User Management** - Registration, login, email verification
- **Password Management** - Password changes, reset via email
- **Email Management** - Change email with verification
- **Role-Based Authorization** - User and admin roles per site
- **API Key Authentication** - Master API key for administrative operations
- **Email Integration** - SendGrid support for transactional emails
- **Token-Based Sessions** - Secure authentication tokens with expiration

## Requirements

- Python 3.13+
- PostgreSQL 12+
- SendGrid account (for email functionality)

## Security Notice

⚠️ **Never use default configuration values in production!**

All configuration must be set via environment variables in production environments:
- Generate a strong random `SECRET_KEY`
- Set a strong `MASTER_API_KEY`
- Use a secure `DB_PASSWORD`
- Configure your `SENDGRID_API_KEY`

See `.env.example` for all required variables.

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your environment variables
3. Set up the database: `python setup-database.py`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python src/app.py`

## Development Status

This project is in early development. APIs and implementation details may change.

## Testing

```bash
pytest
```

## License

MIT
