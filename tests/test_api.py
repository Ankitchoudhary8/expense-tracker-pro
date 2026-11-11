"""Basic API smoke tests. Run: python -m unittest discover -s tests"""
import os
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
        with self.client.session_transaction() as sess:
            sess["authenticated"] = True
            sess["csrf_token"] = "test-csrf"
        self.client.environ_base["HTTP_X_CSRF_TOKEN"] = "test-csrf"

    def tearDown(self):
        self.db_patch.stop()
        self.temp.cleanup()

    def test_unauthorized_requests_blocked(self):
        import app
        anonymous = app.app.test_client()
        self.assertEqual(anonymous.get("/api/expenses").status_code, 401)
        self.assertEqual(anonymous.post("/api/expenses", json={}).status_code, 401)
        self.assertEqual(self.client.post("/api/expenses", json={}, headers={"X-CSRF-Token": "wrong"}).status_code, 403)

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

    def test_edit_expense(self):
        payload = {"title": "Lunch", "amount": 150, "category": "Food", "date": "2026-11-11"}
        created = self.client.post("/api/expenses", json=payload)
        expense_id = created.get_json()["id"]
        payload["amount"] = 250
        response = self.client.put(f"/api/expenses/{expense_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["amount"], 250)
        self.assertEqual(self.client.put("/api/expenses/999", json=payload).status_code, 404)

    def test_monthly_budget(self):
        self.assertIsNone(self.client.get("/api/budgets/2026-11").get_json()["amount"])
        response = self.client.put("/api/budgets/2026-11", json={"amount": 5000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/api/budgets/2026-11").get_json()["amount"], 5000)
        self.assertEqual(self.client.put("/api/budgets/2026-11", json={"amount": -1}).status_code, 400)
        self.assertEqual(self.client.put("/api/budgets/2026-13", json={"amount": 100}).status_code, 400)

    def test_reject_invalid_expense(self):
        response = self.client.post("/api/expenses", json={
            "title": "Invalid", "amount": -1, "category": "Food", "date": "2026-11-11"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
