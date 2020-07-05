import json
from unittest import TestCase

from project import create_app
from project.api.models import Category


class TestCategories(TestCase):
    def setUp(self):
        self.test_app = create_app()
        self.test_app.config.from_object("project.config.TestingConfig")

    def test_get_categories(self):
        with self.test_app.app_context():
            client = self.test_app.test_client()
            resp = client.get(f"/categories")

            self.assertEqual(resp.status_code, 200)

            data = json.loads(resp.data.decode())

            category_query = Category.query.all()
            categories = {str(item.id): item.type.lower() for item in category_query}

            self.assertEqual(data["categories"], categories)
