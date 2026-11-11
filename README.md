# Expense Tracker Pro 💸

A responsive full-stack personal finance dashboard built with **Python, Flask, PostgreSQL (Neon), HTML, CSS, and JavaScript**. SQLite remains available for local development when `DATABASE_URL` is unset.

## 🌐 Live Demo

**[Open Expense Tracker Pro](https://expense-tracker-pro-1-595b.onrender.com)**

> The hosted application requires sign-in. Use your own authorized credentials; never publish passwords or secret keys.

## Features

- Add, edit, and delete expenses with categories and dates
- Monthly budget tracking and spending alerts
- Transaction counts, totals, and average expense
- Month and category filters
- Category donut chart and six-month spending visualization
- CSV export
- Responsive frontend
- Login/logout protection for the hosted application

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | Neon PostgreSQL (production), SQLite (local fallback) |
| Production server | Gunicorn |
| Hosting | Render |
| CI | GitHub Actions |

## Screenshots

Screenshots will be added to the `screenshots/` folder after capturing the deployed interface with non-sensitive sample data.

## Local Setup

```powershell
git clone https://github.com/Ankitchoudhary8/expense-tracker-pro.git
cd expense-tracker-pro
py -m pip install -r backend/requirements.txt
py backend/app.py
```

Open http://127.0.0.1:5000. Before starting the app, set `EXPENSE_APP_PASSWORD` to a private password and `FLASK_SECRET_KEY` to a stable random secret in the local terminal. When `DATABASE_URL` is not set, the application uses a local SQLite database. To develop against PostgreSQL, set `DATABASE_URL` privately using an isolated test database; never copy production credentials into GitHub or screenshots.

## Run Tests

```powershell
py -m unittest discover -s tests -v
```

## Project Structure

```text
backend/
  app.py
  database.py
  requirements.txt
frontend/
  templates/
  static/
tests/
.github/workflows/
Procfile
DEPLOYMENT.md
```

## API

- `GET /api/expenses` — list expenses
- `POST /api/expenses` — create expense
- `PUT /api/expenses/<id>` — edit expense
- `DELETE /api/expenses/<id>` — delete expense
- `GET /api/budgets/<YYYY-MM>` — read a monthly budget
- `PUT /api/budgets/<YYYY-MM>` — save a monthly budget

Mutating endpoints should be accessed through the authenticated interface.

## Deployment and Data Persistence

The app is deployed as a Render **Web Service**, not a static site. See [DEPLOYMENT.md](DEPLOYMENT.md) for configuration and security considerations.

**Production storage:** The live Flask service uses Neon PostgreSQL through Render's secret `DATABASE_URL`. When this setting is absent, the app falls back to SQLite; an ephemeral Render filesystem is not suitable for persistent SQLite storage. The production Postgres setup was verified on 11 November 2026: app tables were present and a sample expense remained available after a Render redeployment and browser refresh.

See [NEON_MIGRATION.md](NEON_MIGRATION.md) for database configuration and safe verification. Expenses can be exported to CSV, but monthly budgets are **not** included in that export. Maintain a separate backup plan for both datasets.

## Project Roadmap

- [x] Phase 1 — Flask API and expense entry
- [x] Phase 2 — Dashboard, charts, filters and CSV export
- [x] Phase 3 — Editing, budgets, alerts and tests
- [x] Phase 4 — CI and deployment configuration
- [x] Phase 5 — Live demo and portfolio documentation
- [ ] Verify all final user journeys and budget calculations
- [ ] Add sanitized application screenshots
- [x] Configure Neon PostgreSQL for durable production storage

## Links

- **Live app:** https://expense-tracker-pro-1-595b.onrender.com
- **CI:** https://github.com/Ankitchoudhary8/expense-tracker-pro/actions
- **Developer:** https://github.com/Ankitchoudhary8
