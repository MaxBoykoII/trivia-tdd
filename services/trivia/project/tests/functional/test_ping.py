from project import app
from unittest import TestCase
import json


class TestPing(TestCase):
    def setUp(self):
        self.test_app = app

    def test_ping(self):
        client = self.test_app.test_client()

        resp = client.get("/ping")
        data = json.loads(resp.data.decode())

        assert resp.status_code == 200
        assert "pong" in data["message"]
        assert "success" in data["status"]
