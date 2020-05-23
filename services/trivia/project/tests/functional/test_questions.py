from project import create_app
from project.api.models import Question, Category
from unittest import TestCase
from parameterized import parameterized
import json


class TestQuestions(TestCase):
    def setUp(self):
        self.test_app = create_app()

    @parameterized.expand([[1], [2], [3], [4]])
    def test_get_questions(self, page):
        with self.test_app.app_context():
            client = self.test_app.test_client()
            resp = client.get(f"/questions?page={page}")

            self.assertEqual(resp.status_code, 200)

            data = json.loads(resp.data.decode())

            per_page = Question.max_results_per_page

            question_query = Question.query.paginate(page, per_page, False)
            questions = [item.format() for item in question_query.items]

            category_ids = [question["category"] for question in questions]
            category_query = Category.query.filter(Category.id.in_(category_ids))
            categories = {
                str(item.id): item.type.lower() for item in category_query.all()
            }

            self.assertEqual(data["questions"], questions)
            self.assertEqual(data["total_questions"], len(questions))
            self.assertIsNone(data["current_category"], None)
            self.assertEqual(data["categories"], categories)
