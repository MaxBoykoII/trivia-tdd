from project import create_app
from unittest import TestCase
import json


class TestPing(TestCase):
    def setUp(self):
        self.test_app = create_app()

    def test_ping(self):
        client = self.test_app.test_client()

        resp = client.get("/ping")
        data = json.loads(resp.data.decode())

        self.assertEqual(resp.status_code, 200)
        self.assertIn("pong", data["message"])
        self.assertIn("success", data["status"])
