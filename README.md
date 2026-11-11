# Expense Tracker Pro 💸

A full-stack expense tracker built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**. Track expenses in Indian rupees with a responsive dashboard.

## Features
- Add expenses with title, amount, category, and date
- View expenses ordered by date
- See total spending in INR
- Delete expenses
- Store expenses locally using SQLite
- Responsive design for mobile and desktop
- JSON REST API with basic input validation

## Project structure
```text
expense-tracker-pro/
├── backend/
│   ├── app.py
│   ├── database.py
│   └── requirements.txt
├── frontend/
│   ├── templates/index.html
│   └── static/
│       ├── app.js
│       └── style.css
├── .gitignore
└── README.md
```

## Run locally (Windows / VS Code)
1. Install Python 3.10+ and Git.
2. Clone and open the project:
   ```powershell
   git clone https://github.com/Ankitchoudhary8/expense-tracker-pro.git
   cd expense-tracker-pro
   code .
   ```
3. Create a virtual environment and install dependencies:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r backend/requirements.txt
   ```
   If PowerShell blocks activation, use `cmd` and run `.venv\Scripts\activate.bat` instead.
4. Start the app:
   ```powershell
   python backend/app.py
   ```
5. Open **http://127.0.0.1:5000** in your browser.

The SQLite database is created automatically at `backend/expenses.db` and is excluded from Git.

## API
| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/expenses` | List expenses |
| POST | `/api/expenses` | Add an expense |
| DELETE | `/api/expenses/<id>` | Delete an expense |

Example POST body:
```json
{"title":"Lunch","amount":150,"category":"Food","date":"2026-11-11"}
```

## Roadmap
- [x] Flask API and SQLite storage
- [x] Expense form and list
- [x] Total spending dashboard
- [ ] Filter by month/category
- [ ] Category breakdown charts
- [ ] CSV export
- [ ] Automated tests and deployment

## Note
This is a learning/portfolio project. The development server is not intended for production deployment.
