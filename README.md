# Egypt SMB Automation API (Security Lab)

Simple Flask API for:
- Leads
- Orders
- Payments

Built for a portfolio/lab project with practical security basics.

## Security Implemented
- Token auth on all `/api/*` routes.
- Token read from `Authorization: Bearer <token>` header.
- No token in query string.
- Security logs with rotating files.
- Token is never written to logs.
- Input validation using Marshmallow schemas.

## Environment Variables
Use `.env.example` values as reference:
- `DATABASE_URL`
- `SECURITY_API_TOKEN`
- `SECURITY_ENFORCE_AUTH`
- `SECURITY_LOG_PATH`

## Run (Source)
1. Install requirements:
```bash
python -m pip install -r automation/requirements_automation.txt
```
2. Set env token (example in PowerShell):
```powershell
$env:SECURITY_API_TOKEN="my-strong-token"
```
3. Run app:
```bash
python -m automation.app
```
4. Health check:
`http://127.0.0.1:8010/health`

## Call Protected Endpoints
Example:
```bash
curl -H "Authorization: Bearer my-strong-token" http://127.0.0.1:8010/api/leads
```

## Project Files
- `automation/app.py`: routes + auth + logging.
- `automation/models.py`: SQLAlchemy models + Marshmallow schemas.
- `automation/config.py`: app and security config.
- `automation_launcher_fixed.py`: EXE entry point.
