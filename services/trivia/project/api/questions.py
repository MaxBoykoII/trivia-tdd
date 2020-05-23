from flask import Blueprint, request
from flask_restx import Resource, Api
from project.api.models import Question, Category

questions_blueprint = Blueprint("questions", __name__)
api = Api(questions_blueprint)


class Questions(Resource):
    def get(self):
        page = int(request.args.get("page"))

        per_page = Question.max_results_per_page

        query = Question.query.paginate(page, per_page, False)
        questions = [item.format() for item in query.items]
        total_questions = len(questions)

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


api.add_resource(Questions, "/questions")
