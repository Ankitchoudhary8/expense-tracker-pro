# Phase 5 — Release Checklist

## Confirmed

- [x] Render web service deployed and accessible
- [x] Hosted sign-in and dashboard observed
- [x] GitHub Actions CI previously shown passing
- [x] README updated with live demo and portfolio description

## Automated verification added

- [x] Added isolated regression tests in `tests/test_release.py` for login/logout, CSRF, expense CRUD, database readback, month-specific budgets, and invalid inputs
- [ ] Confirm the latest GitHub Actions run is green (tests have been committed but execution result is not yet confirmed)
- [ ] Confirm production data survives a service restart/redeploy (not tested; default SQLite storage is ephemeral)

## Manual checks still required

- [ ] Sign in and sign out
- [ ] Add, edit, and delete a test expense
- [ ] Check month and category filtering
- [ ] Download and inspect CSV export
- [ ] Save a budget and compare it to expense totals
- [ ] Verify budget values use the intended month/category scope
- [ ] Test mobile layout
- [ ] Check CI after latest commit

## Screenshots to capture

Create `screenshots/` and save sanitized captures as:

- `dashboard.png`
- `expense-history.png`
- `budget-tracker.png`
- `login.png`

Remove personal transaction details, passwords, tokens, and private account information before uploading.

## Important deployment risks

1. **Data persistence:** SQLite on Render's ephemeral filesystem may be reset on redeploy/restart. Use durable storage or migrate to a managed database.
2. **Budget calculation:** A deployed screenshot showed a ₹20,000 expense total while the budget widget reported ₹40,000 used. Verify whether the widget is aggregating all categories or double-counting before declaring the feature tested.
3. **Secrets:** Use Render environment variables with the exact names expected by `backend/app.py`. Never commit secrets.
4. **Security:** Review authentication, CSRF protection, and session cookie settings before storing real financial data.

## Portfolio-ready project description

**Expense Tracker Pro — Full-Stack Web Application**

Built a responsive expense-management dashboard with Python, Flask, JavaScript, and SQLite. Implemented expense CRUD operations, category/month filters, spending charts, monthly budgets, and CSV export. Added automated tests and GitHub Actions CI, and deployed the application to Render.

**Live demo:** https://expense-tracker-pro-1-595b.onrender.com
