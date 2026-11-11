from datetime import date
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
        if not (0 < amount < 1e12):
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

if __name__ == "__main__":
    app.run(debug=True)
