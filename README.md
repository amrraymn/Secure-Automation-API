A professional Flask-based API designed for small-business automation workflows in Egypt. This project streamlines leads management, order tracking, and payments while implementing practical security layers to protect business data.

## Security Lab Features
I transformed this automation tool into a secure API by implementing:
- Token-based authentication to restrict access to authorized users.
- Input validation and filtering using Marshmallow schemas.
- Security logging and monitoring for unauthorized access attempts.
- Defensive error handling to avoid unnecessary information leakage.

## Core Business Features
- Leads management (create, read, update, delete).
- Orders and due tracking.
- Automatic order status updates (`open`, `partial`, `paid`) based on payments.
- SQLite storage.
- JSON validation and serialization with Marshmallow.

## Tech Stack
- Framework: Flask
- ORM: Flask-SQLAlchemy
- Validation: Flask-Marshmallow / Marshmallow
- Database: SQLite

## Quick Start
1. Install dependencies:
```bash
python -m pip install -r automation/requirements_automation.txt
```

2. Set your API token (PowerShell example):
```powershell
$env:SECURITY_API_TOKEN="my-strong-token"
```

3. Run API:
```bash
python -m automation.app
```

4. Health check:
`http://127.0.0.1:8010/health`

## Protected API Usage
All `/api/*` endpoints require:
```http
Authorization: Bearer <your-token>
```

Example:
```bash
curl -H "Authorization: Bearer my-strong-token" http://127.0.0.1:8010/api/leads
```

## Project Structure
- `automation/app.py`: App factory and secure API routes.
- `automation/models.py`: Database models and schemas.
- `automation/config.py`: Environment and security configuration.
- `automation_launcher_fixed.py`: Desktop/EXE entry point.

## Latest Security Fixes (Review Update)
This section summarizes the fixes applied after code review:

1. Authentication is now centralized and enforced across all protected `/api/*` endpoints.
2. Hardcoded/query-string token usage was removed; token now comes from environment variables and `Authorization: Bearer` header.
3. Security logs were improved to avoid token leakage and sanitize untrusted input before logging.
4. Documentation was aligned with the real implementation so security behavior matches what is described.

