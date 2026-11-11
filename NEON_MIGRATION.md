# Neon PostgreSQL migration (staged, not yet live)

The application uses SQLite when `DATABASE_URL` is absent and Neon PostgreSQL when it is present. PostgreSQL support is staged on the `feature/neon-postgres-persistence` branch to avoid accidentally switching the live Render service.

## Before activating

1. Rotate the Neon database role password because a previous screenshot exposed its connection string. Never commit connection URLs, passwords, or `.env` files.
2. Back up existing SQLite records **including budgets**. CSV export covers expenses only. A new Neon database starts empty; this change does **not** migrate historical records.
3. Run CI and verify the application using a disposable PostgreSQL database, including expense create/edit/delete, budgets, authentication, and persistence after restart.
4. Merge the feature branch after testing. In Render > Web Service > Environment, set `DATABASE_URL` to the **new** Neon pooled PostgreSQL connection string with TLS (`sslmode=require`). Use Render's secret environment variables, never source code. Remove `EXPENSE_DB_PATH` if it points to a nonexistent disk.
5. Redeploy, verify the live app, and check data survives a Render restart/redeploy. Restore existing records via a deliberate migration before treating the new database as authoritative.

**Do not set DATABASE_URL on the live service before the migration plan is complete.** Keep the existing Render Free web service. Neon Free plan limits and inactivity policies may change; monitor usage and arrange backups.
