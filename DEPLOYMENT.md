# Security and deployment preparation

## Local setup (PowerShell)

Stop the Flask server, then run:

```powershell
git pull origin main
$env:EXPENSE_APP_PASSWORD = "replace-with-a-long-unique-password"
$env:FLASK_SECRET_KEY = py -c "import secrets; print(secrets.token_hex(32))"
py -m unittest discover -s tests -v
py backend/app.py
```

Open http://127.0.0.1:5000 and sign in with your password. The variables above last only for the current PowerShell terminal session. Do not paste passwords into chat or commit them to Git.

## Security controls

- All expense and budget API endpoints require an authenticated session.
- State-changing API requests require a per-session CSRF token.
- Session cookies are HTTP-only and SameSite=Lax.
- Flask debug mode is off by default.
- Logout invalidates the session.
- Single shared password only: this is **not** a multi-user product, has no rate limiting, and is not suitable for storing sensitive financial data on an open public host without additional hardening.

## Production environment variables

Set these privately in your hosting provider's environment/secrets configuration:

- `EXPENSE_APP_PASSWORD`: long, unique password, never committed to Git.
- `FLASK_SECRET_KEY`: stable random secret (at least 32 random bytes represented as hex). Keep it stable across restarts.
- `COOKIE_SECURE=1`: required when served over HTTPS.
- `FLASK_DEBUG=0`.
- `EXPENSE_DB_PATH`: full path to SQLite file on a persistent mounted disk.

SQLite on an ephemeral host loses data on restart/redeploy. Configure a persistent volume with backups or migrate to managed PostgreSQL before any serious use.

## Deployment

The repo includes `Procfile`, `.python-version`, and `gunicorn`.

- Runtime: Python 3.12, Linux.
- Build command: `pip install -r backend/requirements.txt`
- Start command: `gunicorn --chdir backend app:app --bind 0.0.0.0:${PORT:-8000}`
- Configure environment variables and persistent storage before deploying.
- Verify HTTPS, login/logout, CSRF rejection, CI status, and data persistence after restart.

**No live hosting has been configured by these commits.** Do not expose personal financial information until these requirements are met.
