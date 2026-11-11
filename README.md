# Expense Tracker Pro 💸

A responsive expense-tracking dashboard built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**.

## Features
- Add, edit, and delete expenses with categories and dates
- Set a monthly spending budget, track progress, and receive 80% / over-budget warnings
- View spending totals, transaction counts, and average expense
- Filter expenses by month and category
- Interactive category breakdown donut chart and six-month spending bars
- Export filtered expenses as a CSV report
- Local SQLite storage and REST API

## Run locally (Windows)
```powershell
git clone https://github.com/Ankitchoudhary8/expense-tracker-pro.git
cd expense-tracker-pro
py -m pip install -r backend/requirements.txt
py backend/app.py
```
Open http://127.0.0.1:5000 in your browser.

If you already cloned the project, stop the server with Ctrl+C, run `git pull origin main` inside the project folder, and restart with `py backend/app.py`. Your local SQLite database is not overwritten.

## Structure
```text
backend/
  app.py
  database.py
  requirements.txt
frontend/
  templates/index.html
  static/app.js
  static/style.css
```

## API
- `GET /api/expenses` — list expenses
- `POST /api/expenses` — create expense
- `DELETE /api/expenses/<id>` — delete expense
- `PUT /api/expenses/<id>` — edit expense
- `GET /api/budgets/<YYYY-MM>` — read a monthly budget
- `PUT /api/budgets/<YYYY-MM>` — save a monthly budget

The dashboard charts and CSV export are computed in the browser from the API data. The SQLite file `backend/expenses.db` is ignored by Git.

## Roadmap
- [x] Phase 1: Flask API, SQLite and expense entry
- [x] Phase 2: Dashboard, category chart, monthly report and CSV export
- [x] Phase 3: Expense editing, monthly budgets, alerts and API tests
- [ ] Phase 4: Deployment and CI/CD

**Development only:** Flask's built-in debug server is not intended for production use.

## Run tests
```powershell
py -m unittest discover -s tests -v
```
