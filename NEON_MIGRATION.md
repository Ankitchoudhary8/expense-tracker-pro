# Neon PostgreSQL production persistence

## Current status (verified 11 November 2026)

**Production is live on Neon PostgreSQL.** The Flask service `expense-tracker-pro-1` on Render is deployed from the GitHub `main` branch. Its secret `DATABASE_URL` points to the `neondb` database in the `production` branch of the existing Neon project.

Verified:
- PostgreSQL driver is installed from `backend/requirements.txt`.
- The deployed Flask app initialized the `expenses` and `budgets` tables in `neondb`.
- A non-sensitive sample expense remained in Neon after a Render redeployment and was visible after refreshing the live dashboard.
- A separate `expense_tracker_test` **database** was used to test expense and budget persistence across database connections. This database is on the same Neon branch; it is not a separate Neon branch.

Still recommended:
- Test saving a monthly budget from the live UI, refreshing and redeploying, then verify the saved budget remains.
- Test create, edit, and delete expense flows and login/logout on production.
- Set up a regular backup process that includes both `expenses` and `budgets`; the CSV export covers expenses only.
- Keep `FLASK_SECRET_KEY` stable across Render restarts, and use `COOKIE_SECURE=1` for HTTPS.
- Rotate database credentials immediately if they are ever exposed.

## Connection settings

The application uses PostgreSQL whenever `DATABASE_URL` is set, otherwise it uses a local SQLite file. This fallback is useful locally but unsafe as durable storage on Render's ephemeral filesystem.

- For the live web service use a **pooled** Neon PostgreSQL connection string (host containing `-pooler`) with `sslmode=require`.
- For schema migrations, database restores, or administrative tasks use a **direct** Neon connection in a trusted environment.
- Set connection credentials only as secret environment variables in Render or privately in a local terminal. Never write them in `.py` files, committed `.env` files, screenshots, logs, or documentation.
- Production database: `neondb`. Test database: `expense_tracker_test`. Check the target database name before any test that writes records.

## Production deployment settings

- Render web service: `expense-tracker-pro-1`
- Runtime: Python
- Branch: `main` (automatic deployment on commit)
- Build command: `pip install -r backend/requirements.txt`
- Start command: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT`
- Secret setting: `DATABASE_URL` (Neon production URL; never commit or display its value)

Changing Render environment variables may trigger an automatic redeployment. Code commits to `main` also trigger a deployment, so review GitHub pull requests before merging.

## Non-destructive verification

In Neon's SQL editor, select the `production` branch and `neondb`. To check connectivity and record totals without modifying data, use:

```sql
SELECT
  current_database() AS database_name,
  (SELECT COUNT(*) FROM public.expenses) AS expense_count,
  (SELECT COUNT(*) FROM public.budgets) AS budget_count;
```

This should return `neondb`. Never run the disposable test script against `neondb`.

## Data safety

The application is designed for one owner, with a single shared password. It is **not a hardened multi-user finance application** and does not have rate limiting.

- Keep exported personal finance data outside the public repository.
- `migration_backup/` is excluded from Git; keep private backups elsewhere as well.
- Do not assume CSV exports preserve budgets, user settings, or schema.
- Do not delete suspected duplicate expenses without confirming which transactions are real.
