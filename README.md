# ByteForge Aegis

Multi-tenant authentication service built with Flask and PostgreSQL. Provides secure user authentication, email verification, password management, and role-based authorization for multiple sites with isolated user bases.

## Features

- **Multi-tenant Architecture** - Isolate users and authentication by site/domain
- **User Management** - Registration, login, email verification
- **Password Management** - Password changes, reset via email
- **Email Management** - Change email with verification
- **Role-Based Authorization** - User and admin roles per site
- **API Key Authentication** - Master API key for administrative operations
- **Email Integration** - Mailgun integration for transactional emails
- **Token-Based Sessions** - Secure authentication tokens with expiration
- **PostgreSQL Backend** - Reliable data storage with proper indexing

## Requirements

- Python 3.13+
- PostgreSQL 12+
- Mailgun account (for email functionality)

## Security Notice

⚠️ **Never use default configuration values in production!**

All configuration must be set via environment variables in production environments:
- Generate a strong random `SECRET_KEY`
- Set a strong `MASTER_API_KEY`
- Use a secure `DB_PASSWORD`
- Configure your `MAILGUN_API_KEY` and `MAILGUN_DOMAIN`

See `.env.example` for all required variables.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/jmazzahacks/byteforge-aegis.git
   cd byteforge-aegis
   ```

2. **Set up Python virtual environment** (already included)
   ```bash
   # Virtual environment is included in the repository
   # Activate it for all commands
   source bin/activate
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and configure your settings
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database and user in PostgreSQL
   psql -U postgres -c "CREATE DATABASE aegis;"
   psql -U postgres -c "CREATE USER aegis_admin WITH PASSWORD 'your-secure-password';"
   psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE aegis TO aegis_admin;"

   # Load schema
   psql -U aegis_admin -d aegis -f database/schema.sql
   ```

5. **Install dependencies**
   ```bash
   source bin/activate && pip install -r requirements.txt
   ```

6. **Run the application**
   ```bash
   source bin/activate && python src/app.py
   ```

The API will be available at `http://localhost:5678`

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

## Admin Scripts

Convenient interactive scripts for common administrative tasks:

- **create-site.py** - Create a new tenant site
- **create-user.py** - Create users (regular or admin) for existing sites
- **test-email-service.py** - Test Mailgun email integration

All scripts use the master API key for authentication. Run from the repository root:

```bash
source bin/activate && python admin_scripts/<script-name>.py
```

## Testing

Run the test suite:

```bash
source bin/activate && pytest
```

Run a specific test:

```bash
source bin/activate && pytest tests/test_specific_file.py::test_function_name
```

## Related Projects

- **byteforge-aegis-client-js** - JavaScript/TypeScript API client
- **byteforge-aegis-frontend** - Next.js frontend application (coming soon)

## Development Status

This project is under active development. APIs and implementation details may change.

## License

MIT

## Author

Jason Byteforge (@jmazzahacks)
