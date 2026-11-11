# Expense Tracker Pro 💸

A responsive full-stack personal finance dashboard built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**.

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
| Database | SQLite |
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

Open http://127.0.0.1:5000. Configure authentication environment variables required by your version of `backend/app.py` before starting it. Do not commit credentials.

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

**Important:** The default SQLite database lives on the service filesystem. Render instances without persistent storage can lose SQLite data during redeploys or restarts. Use durable storage or migrate to a managed database before relying on the app for real financial records.

## Project Roadmap

- [x] Phase 1 — Flask API and expense entry
- [x] Phase 2 — Dashboard, charts, filters and CSV export
- [x] Phase 3 — Editing, budgets, alerts and tests
- [x] Phase 4 — CI and deployment configuration
- [x] Phase 5 — Live demo and portfolio documentation
- [ ] Verify all final user journeys and budget calculations
- [ ] Add sanitized application screenshots
- [ ] Configure durable database storage

## Links

- **Live app:** https://expense-tracker-pro-1-595b.onrender.com
- **CI:** https://github.com/Ankitchoudhary8/expense-tracker-pro/actions
- **Developer:** https://github.com/Ankitchoudhary8
