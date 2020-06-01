import json
from unittest import TestCase

from project import create_app


class TestPing(TestCase):
    def setUp(self):
        self.test_app = create_app()
        self.test_app.config.from_object("project.config.TestingConfig")

    def test_ping(self):
        client = self.test_app.test_client()

        resp = client.get("/ping")
        data = json.loads(resp.data.decode())

        self.assertEqual(resp.status_code, 200)
        self.assertIn("pong", data["message"])
        self.assertIn("success", data["status"])
