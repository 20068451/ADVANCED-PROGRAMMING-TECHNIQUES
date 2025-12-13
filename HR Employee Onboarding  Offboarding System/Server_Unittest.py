import unittest
from unittest.mock import patch
from datetime import date, timedelta

import Server


class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_values=None):
        self._fetchone_values = fetchone_values or []
        self._fetchall_values = fetchall_values or []
        self._fetchone_i = 0
        self._fetchall_i = 0
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        return self

    def fetchone(self):
        if self._fetchone_i < len(self._fetchone_values):
            v = self._fetchone_values[self._fetchone_i]
            self._fetchone_i += 1
            return v
        return None

    def fetchall(self):
        if self._fetchall_i < len(self._fetchall_values):
            v = self._fetchall_values[self._fetchall_values.index(self._fetchall_values[self._fetchall_i])]
            self._fetchall_i += 1
            return v
        return []


class FakeConn:
    def __init__(self, cursor: FakeCursor):
        self._cursor = cursor
        self.committed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def auth_header(token="simple-token"):
    return {"Authorization": f"Bearer {token}"}


class TestEmployeeSystem11(unittest.TestCase):
    def setUp(self):
        Server.app.testing = True
        self.client = Server.app.test_client()

    def test_01_login_missing_fields(self):
        res = self.client.post("/login", json={})
        self.assertEqual(res.status_code, 400)

    @patch("Server.get_connection")
    def test_02_login_invalid_user(self, mock_get_connection):
        fake_cur = FakeCursor(fetchone_values=[None])
        mock_get_connection.return_value = FakeConn(fake_cur)

        res = self.client.post("/login", json={"username": "wrong", "password": "x"})
        self.assertEqual(res.status_code, 401)

    @patch("Server.get_connection")
    def test_03_login_success(self, mock_get_connection):
        stored_hash = Server.hash_password("pass")
        fake_cur = FakeCursor(fetchone_values=[(stored_hash,)])
        mock_get_connection.return_value = FakeConn(fake_cur)

        res = self.client.post("/login", json={"username": "admin", "password": "pass"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json().get("token"), "simple-token")

    def test_04_employees_unauthorized(self):
        res = self.client.get("/employees")
        self.assertEqual(res.status_code, 401)

    def test_05_onboard_invalid_ppsn(self):
        payload = {
            "name": "John",
            "doj": str(date.today()),
            "address": "Dublin",
            "ppsn": "123",
            "position": "Dev",
            "department": "IT",
            "asset_ids": []
        }
        res = self.client.post("/onboard", json=payload, headers=auth_header())
        self.assertEqual(res.status_code, 400)

    def test_06_onboard_past_date(self):
        payload = {
            "name": "John",
            "doj": str(date.today() - timedelta(days=1)),
            "address": "Dublin",
            "ppsn": "123456789",
            "position": "Dev",
            "department": "IT",
            "asset_ids": []
        }
        res = self.client.post("/onboard", json=payload, headers=auth_header())
        self.assertEqual(res.status_code, 400)

    @patch("Server.get_connection")
    def test_07_onboard_success(self, mock_get_connection):
        class ERow:
            employee_id = "2000-006"
            name = "Jane"
            date_of_joining = date.today()
            address = "Dublin"
            ppsn = "123456789"
            position = "Analyst"
            department = "IT"
            status = "ACTIVE"

        fake_cur = FakeCursor(
            fetchone_values=[("2000-005",), ERow()],
            fetchall_values=[[]]
        )
        mock_get_connection.return_value = FakeConn(fake_cur)

        payload = {
            "name": "Jane",
            "doj": str(date.today()),
            "address": "Dublin",
            "ppsn": "123456789",
            "position": "Analyst",
            "department": "IT",
            "asset_ids": []
        }
        res = self.client.post("/onboard", json=payload, headers=auth_header())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["employee"]["status"], "ACTIVE")

    def test_08_offboard_missing_employee_id(self):
        res = self.client.post("/offboard", json={}, headers=auth_header())
        self.assertEqual(res.status_code, 400)

    @patch("Server.get_connection")
    def test_09_offboard_not_found(self, mock_get_connection):
        fake_cur = FakeCursor(fetchone_values=[None])
        mock_get_connection.return_value = FakeConn(fake_cur)

        res = self.client.post("/offboard", json={"employee_id": "2000-999"}, headers=auth_header())
        self.assertEqual(res.status_code, 404)

    def test_10_monthly_report_missing_params(self):
        res = self.client.get("/report/monthly", headers=auth_header())
        self.assertEqual(res.status_code, 400)

    @patch("Server.get_connection")
    def test_11_stats_success(self, mock_get_connection):
        fake_cur = FakeCursor(fetchone_values=[(5,), (10,), (7,), (3,), (2, 1)])
        mock_get_connection.return_value = FakeConn(fake_cur)

        res = self.client.get("/stats", headers=auth_header())
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["active_employees"], 5)
        self.assertEqual(data["assigned_assets"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
