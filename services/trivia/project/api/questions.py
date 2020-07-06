from flask import Blueprint, request
from flask_restx import Api, Resource
from project.api.models import Category, Question

questions_blueprint = Blueprint("questions", __name__)
api = Api(questions_blueprint)


class Questions(Resource):
    def get(self):
        page = int(request.args.get("page"))

        per_page = Question.max_results_per_page

        query = Question.query.paginate(page, per_page, False)
        questions = [item.format() for item in query.items]
        total_questions = Question.query.count()

        current_category = None

        category_ids = [question["category"] for question in questions]
        category_query = Category.query.filter(Category.id.in_(category_ids))
        categories = {item.id: item.type.lower() for item in category_query.all()}

        payload = {
            "questions": questions,
            "total_questions": total_questions,
            "current_category": current_category,
            "categories": categories,
        }

        return payload, 200

    def post(self):
        post_data = request.get_json()

        question = Question(
            post_data.get("question"),
            post_data.get("answer"),
            post_data.get("category"),
            post_data.get("difficulty"),
        )
        question.insert()

        return question.id, 201


api.add_resource(Questions, "/questions")
