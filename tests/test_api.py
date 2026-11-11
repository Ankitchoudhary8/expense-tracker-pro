"""Basic API smoke tests. Run: python -m unittest discover -s tests"""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
import database

class ExpenseAPITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_patch = patch.object(database, "DB_PATH", Path(self.temp.name) / "test.db")
        self.db_patch.start()
        database.init_db()
        import app
        self.client = app.app.test_client()

    def tearDown(self):
        self.db_patch.stop()
        self.temp.cleanup()

    def test_create_list_delete(self):
        response = self.client.post("/api/expenses", json={
            "title": "Lunch", "amount": 150, "category": "Food", "date": "2026-11-11"
        })
        self.assertEqual(response.status_code, 201)
        expense_id = response.get_json()["id"]
        response = self.client.get("/api/expenses")
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(self.client.delete(f"/api/expenses/{expense_id}").status_code, 200)
        self.assertEqual(self.client.get("/api/expenses").get_json(), [])

    def test_reject_invalid_expense(self):
        response = self.client.post("/api/expenses", json={
            "title": "Invalid", "amount": -1, "category": "Food", "date": "2026-11-11"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
