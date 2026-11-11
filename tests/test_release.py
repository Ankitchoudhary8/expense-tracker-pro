"""Release regression tests using an isolated temporary SQLite database.

Run: python -m unittest discover -s tests -v
No requests are made to the deployed application.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
import database
import app as application


class ReleaseVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "release-test.db"
        self.db_patch = patch.object(database, "DB_PATH", self.db_path)
        self.db_patch.start()
        database.init_db()
        self.client = application.app.test_client()

    def tearDown(self):
        self.db_patch.stop()
        self.temp.cleanup()

    def authenticate(self):
        with self.client.session_transaction() as session:
            session["authenticated"] = True
            session["csrf_token"] = "release-test-token"

    def test_login_logout_and_protected_dashboard(self):
        self.assertEqual(self.client.get("/").status_code, 302)
        self.assertEqual(self.client.get("/login").status_code, 200)
        with patch.dict(os.environ, {"EXPENSE_APP_PASSWORD": "local-test-password"}):
            self.assertEqual(self.client.post("/login", data={"password": "wrong"}).status_code, 401)
            self.assertEqual(self.client.post("/login", data={"password": "local-test-password"}).status_code, 302)
            self.assertEqual(self.client.get("/").status_code, 200)
            self.assertEqual(self.client.post("/logout", data={"csrf_token": "incorrect"}).status_code, 403)
            with self.client.session_transaction() as session:
                token = session["csrf_token"]
            self.assertEqual(self.client.post("/logout", data={"csrf_token": token}).status_code, 302)
            self.assertEqual(self.client.get("/api/expenses").status_code, 401)

    def test_expense_crud_persists_across_clients(self):
        self.authenticate()
        payload = {"title": "Verification lunch", "amount": 125.5, "category": "Food", "date": "2026-11-11"}
        created = self.client.post("/api/expenses", json=payload, headers={"X-CSRF-Token": "release-test-token"})
        self.assertEqual(created.status_code, 201)
        expense_id = created.get_json()["id"]
        another_client = application.app.test_client()
        with another_client.session_transaction() as session:
            session["authenticated"] = True
            session["csrf_token"] = "another-token"
        self.assertEqual(len(another_client.get("/api/expenses").get_json()), 1)
        payload["amount"] = 200
        self.assertEqual(self.client.put(f"/api/expenses/{expense_id}", json=payload, headers={"X-CSRF-Token": "release-test-token"}).status_code, 200)
        self.assertEqual(another_client.get("/api/expenses").get_json()[0]["amount"], 200)
        self.assertEqual(self.client.delete(f"/api/expenses/{expense_id}", headers={"X-CSRF-Token": "release-test-token"}).status_code, 200)
        self.assertEqual(another_client.get("/api/expenses").get_json(), [])
        self.assertEqual(self.client.delete(f"/api/expenses/{expense_id}", headers={"X-CSRF-Token": "release-test-token"}).status_code, 404)

    def test_budget_is_stored_per_month(self):
        self.authenticate()
        headers = {"X-CSRF-Token": "release-test-token"}
        self.assertEqual(self.client.put("/api/budgets/2026-11", json={"amount": 1000}, headers=headers).status_code, 200)
        self.assertEqual(self.client.put("/api/budgets/2026-12", json={"amount": 2500}, headers=headers).status_code, 200)
        self.assertEqual(self.client.get("/api/budgets/2026-11").get_json()["amount"], 1000)
        self.assertEqual(self.client.get("/api/budgets/2026-12").get_json()["amount"], 2500)
        self.assertEqual(self.client.put("/api/budgets/2026-11", json={"amount": 1500}, headers=headers).status_code, 200)
        self.assertEqual(self.client.get("/api/budgets/2026-11").get_json()["amount"], 1500)
        self.assertEqual(self.client.get("/api/budgets/2026-12").get_json()["amount"], 2500)

    def test_invalid_amounts_and_csrf_rejected(self):
        self.authenticate()
        payload = {"title": "Test", "amount": 10, "category": "Food", "date": "2026-11-11"}
        self.assertEqual(self.client.post("/api/expenses", json=payload).status_code, 403)
        headers = {"X-CSRF-Token": "release-test-token"}
        for invalid in [-1, 0, float("inf"), float("nan")]:
            payload["amount"] = invalid
            with self.subTest(amount=str(invalid)):
                self.assertEqual(self.client.post("/api/expenses", json=payload, headers=headers).status_code, 400)
        payload["amount"] = 10
        payload["date"] = "not-a-date"
        self.assertEqual(self.client.post("/api/expenses", json=payload, headers=headers).status_code, 400)
        self.assertEqual(self.client.get("/api/budgets/2026-13").status_code, 400)

    def test_security_cookie_configuration(self):
        self.assertTrue(application.app.config["SESSION_COOKIE_HTTPONLY"])
        self.assertEqual(application.app.config["SESSION_COOKIE_SAMESITE"], "Lax")


if __name__ == "__main__":
    unittest.main()
