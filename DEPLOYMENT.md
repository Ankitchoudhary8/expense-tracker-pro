# Deployment guide

## Important security and storage limitations

**Do not publish this application with real financial data yet.** The current API has no authentication: anyone who knows the public URL can view, add, edit, and delete the expenses and budgets stored by the application. A production release requires authentication and authorization.

SQLite is stored on the server filesystem. On many free or ephemeral hosting plans, data may disappear after redeploys/restarts. Use a persistent disk mounted at a configured location, or migrate to a managed database before storing valuable data. Never commit a real `expenses.db` file.

## Production-ready server command

The repository includes `gunicorn` in requirements and a `Procfile`:

```sh
gunicorn --chdir backend app:app --bind 0.0.0.0:${PORT:-8000}
```

Use a Linux Python web service with Python 3.12. Configure its start command to the command above. Install dependencies with:

```sh
pip install -r backend/requirements.txt
```

## Deployment checklist

1. Confirm the GitHub Actions CI workflow passes.
2. Implement user authentication and restrict all expense and budget API endpoints before any public release.
3. Configure a persistent storage volume or migrate to PostgreSQL.
4. Set `EXPENSE_DB_PATH` to a writable path on persistent storage if using SQLite.
5. Set `FLASK_DEBUG=0` and run Gunicorn (never use Flask's development server publicly).
6. Configure HTTPS, secrets, backups, and error monitoring.
7. Deploy from GitHub through your chosen host's dashboard and verify health and data persistence.

No live service is deployed by committing these files alone.
