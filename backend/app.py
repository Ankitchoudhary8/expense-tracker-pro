from datetime import date
import math
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from database import get_connection, init_db

BASE_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR.parent / "frontend" / "templates"),
    static_folder=str(BASE_DIR.parent / "frontend" / "static"),
)
init_db()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/expenses")
def list_expenses():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, amount, category, date FROM expenses ORDER BY date DESC, id DESC"
        ).fetchall()
    return jsonify([dict(row) for row in rows])

@app.post("/api/expenses")
def create_expense():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    category = str(data.get("category", "")).strip()
    expense_date = str(data.get("date", "")).strip()
    try:
        amount = float(data.get("amount", 0))
        if not (math.isfinite(amount) and 0 < amount < 1e12):
            raise ValueError
        date.fromisoformat(expense_date)
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid positive amount and date."}), 400
    if not title or not category or len(title) > 120 or len(category) > 50:
        return jsonify({"error": "Title and category are required."}), 400
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
            (title, amount, category, expense_date),
        )
        connection.commit()
        expense_id = cursor.lastrowid
    return jsonify({"id": expense_id, "title": title, "amount": amount, "category": category, "date": expense_date}), 201

@app.delete("/api/expenses/<int:expense_id>")
def delete_expense(expense_id):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Expense not found."}), 404
    return jsonify({"message": "Expense deleted."})


@app.put("/api/expenses/<int:expense_id>")
def update_expense(expense_id):
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    category = str(data.get("category", "")).strip()
    expense_date = str(data.get("date", "")).strip()
    try:
        amount = float(data.get("amount", 0))
        if not (math.isfinite(amount) and 0 < amount < 1e12):
            raise ValueError
        date.fromisoformat(expense_date)
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid positive amount and date."}), 400
    if not title or not category or len(title) > 120 or len(category) > 50:
        return jsonify({"error": "Title and category are required."}), 400
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE expenses SET title = ?, amount = ?, category = ?, date = ? WHERE id = ?",
            (title, amount, category, expense_date, expense_id),
        )
        connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Expense not found."}), 404
    return jsonify({"id": expense_id, "title": title, "amount": amount, "category": category, "date": expense_date})

@app.get("/api/budgets/<month>")
def get_budget(month):
    try:
        if len(month) != 7 or date.fromisoformat(month + "-01").strftime("%Y-%m") != month:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid month."}), 400
    with get_connection() as connection:
        row = connection.execute("SELECT amount FROM budgets WHERE month = ?", (month,)).fetchone()
    return jsonify({"month": month, "amount": row["amount"] if row else None})

@app.put("/api/budgets/<month>")
def set_budget(month):
    try:
        if len(month) != 7 or date.fromisoformat(month + "-01").strftime("%Y-%m") != month:
            raise ValueError
        amount = float((request.get_json(silent=True) or {}).get("amount"))
        if not (math.isfinite(amount) and 0 < amount < 1e12):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid month and positive budget."}), 400
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO budgets (month, amount) VALUES (?, ?) ON CONFLICT(month) DO UPDATE SET amount = excluded.amount",
            (month, amount),
        )
        connection.commit()
    return jsonify({"month": month, "amount": amount})

if __name__ == "__main__":
    app.run(debug=True)
