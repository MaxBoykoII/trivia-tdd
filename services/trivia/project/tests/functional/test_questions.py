import json
from unittest import TestCase

from parameterized import parameterized
from project import create_app, db
from project.api.models import Category, Question


class TestQuestions(TestCase):
    def setUp(self):
        self.test_app = create_app()
        self.test_app.config.from_object("project.config.TestingConfig")

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
            self.assertEqual(data["total_questions"], Question.query.count())
            self.assertIsNone(data["current_category"], None)
            self.assertEqual(data["categories"], categories)

    def test_add_question(self):
        with self.test_app.app_context():
            request_data = {
                "question": "Who was the 30th president of the United States?",
                "answer": "Calvin Coolidge",
                "difficulty": 4,
                "category": 4,
            }
            client = self.test_app.test_client()
            resp = client.post(
                "/questions",
                data=json.dumps(request_data),
                content_type="application/json",
            )

            self.assertEqual(resp.status_code, 201)

            question = Question.query.filter(
                Question.question == request_data["question"]
            ).first()

            self.assertIsNotNone(question)

            question_data = vars(question)

            for key, val in request_data.items():
                self.assertEqual(val, question_data[key])

            db.session.delete(question)
            db.session.commit()
