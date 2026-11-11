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
- `DATABASE_URL`: pooled Neon PostgreSQL connection URL with TLS, stored privately on Render. This is the production database configuration.
- `EXPENSE_DB_PATH`: optional SQLite-only database location for local development or a mounted SQLite disk. Not required for Neon.

The live service uses Neon PostgreSQL, avoiding data loss from Render's ephemeral local SQLite filesystem. Set up separate backups for both expenses and monthly budgets.

## Deployment

The repo includes `Procfile`, `.python-version`, and `gunicorn`.

- Runtime: Python 3.12, Linux.
- Build command: `pip install -r backend/requirements.txt`
- Start command: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT`
- Configure required environment variables securely before deploying; the production database is Neon PostgreSQL.
- Verify HTTPS, login/logout, CSRF rejection, CI status, and data persistence after restart.

**Live deployment:** The `expense-tracker-pro-1` service on Render has Neon `DATABASE_URL` configured. The PostgreSQL-backed deployment and sample expense persistence through a Render redeployment were verified on 11 November 2026. Keep access controls enabled and do not expose personal financial information.

## Production persistence with Neon PostgreSQL

The live Flask web service `expense-tracker-pro-1` uses Neon PostgreSQL in database `neondb`, configured through Render's private `DATABASE_URL`. Its code is deployed from `main`, and commits to `main` trigger automatic deployments. The build and start commands are listed above.

1. In Neon, use the `production` branch and the `neondb` database. The `expense_tracker_test` database is reserved for isolated tests and must not be used by the live service.
2. Keep `DATABASE_URL` in Render's Environment settings as a secret. Prefer Neon's pooled connection URL with `sslmode=require`. Do not copy connection credentials into source code or screenshots.
3. Keep `EXPENSE_APP_PASSWORD` private and `FLASK_SECRET_KEY` stable; use `COOKIE_SECURE=1` over HTTPS.
4. A sample expense was verified through the live site, and checked in Neon after a full Render redeployment. Production budget persistence through a redeployment has not yet been verified end-to-end.
5. Back up both expenses and monthly budgets regularly. The app's CSV export contains expenses only.

When `DATABASE_URL` is absent, the app falls back to SQLite. Render's free web-service filesystem is ephemeral, so this fallback must not be relied upon for production persistence. See [NEON_MIGRATION.md](NEON_MIGRATION.md) for safe verification and database management.

## Budget calculation definition

The spending summary honors the selected month **and category**. The monthly budget is for the selected month across **all categories**, even when a category filter is active. For example, Food ₹20,000 and Bills ₹20,000 yield filtered Food spending of ₹20,000 but total budget spending of ₹40,000. The dashboard now explicitly labels the budget total as all categories, and regression tests check this arithmetic. Changing months clears the previous month's budget display until the new value loads.
