from project import create_app, db
from project.api.models import Question
from unittest import TestCase
from parameterized import parameterized
import json


class TestQuestions(TestCase):
    def setUp(self):
        self.test_app = create_app()
        self.db = db

    @parameterized.expand([[1], [2], [3], [4]])
    def test_get_questions(self, page):
        with self.test_app.app_context():
            client = self.test_app.test_client()
            resp = client.get(f"/questions?page={page}")

            self.assertEqual(resp.status_code, 200)

            data = json.loads(resp.data.decode())

            per_page = Question.max_results_per_page

            query = self.db.session.query(Question).paginate(page, per_page, False)
            questions = [item.format() for item in query.items]

            for i in range(len(questions)):
                self.assertDictEqual(data[i], questions[i])
