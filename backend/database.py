import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(os.environ.get("EXPENSE_DB_PATH", str(Path(__file__).resolve().parent / "expenses.db"))).expanduser()

# A mounted volume must exist before deployment; never silently fall back to ephemeral storage.
def validate_database_location():
    if os.environ.get("EXPENSE_DB_PATH"):
        parent = DB_PATH.parent
        if not parent.is_dir():
            raise RuntimeError(f"Database directory does not exist: {parent}. Mount persistent storage before starting.")
        if not os.access(parent, os.W_OK):
            raise RuntimeError(f"Database directory is not writable: {parent}")

@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def init_db():
    validate_database_location()
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                month TEXT PRIMARY KEY,
                amount REAL NOT NULL CHECK(amount > 0)
            )
        """)
        connection.commit()
