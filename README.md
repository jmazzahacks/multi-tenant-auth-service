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
2. Copy `env.example` to `.env` and configure your environment variables
3. Set up the database: `python setup-database.py`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python src/app.py`

## API Documentation

### Site Management

Site management endpoints require the master API key (`X-API-Key` header).

#### Create Site

Create a new tenant site. Use the included interactive script for convenience.

```bash
# Using the interactive script
python admin_scripts/create-site.py

# Or using curl directly
curl -X POST http://localhost:5678/api/sites \
  -H "X-API-Key: your-master-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Website",
    "domain": "example.com",
    "frontend_url": "https://example.com",
    "email_from": "noreply@example.com",
    "email_from_name": "My Website"
  }'
```

#### List All Sites

```bash
curl http://localhost:5678/api/sites \
  -H "X-API-Key: your-master-api-key"
```

#### Get Site by ID

```bash
curl http://localhost:5678/api/sites/{site_id} \
  -H "X-API-Key: your-master-api-key"
```

#### Get Site by Domain (Public)

This endpoint is public to allow frontend applications to bootstrap by looking up their site configuration.

```bash
curl "http://localhost:5678/api/sites/by-domain?domain=example.com"
```

#### Update Site

All fields are optional. Only provided fields will be updated.

```bash
curl -X PUT http://localhost:5678/api/sites/{site_id} \
  -H "X-API-Key: your-master-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "email_from": "support@example.com",
    "email_from_name": "Support Team"
  }'
```

### User Management

User management endpoints are scoped to sites and use bearer token authentication.

Documentation coming soon.

## Development Status

This project is in early development. APIs and implementation details may change.

## Testing

```bash
pytest
```

## License

MIT
