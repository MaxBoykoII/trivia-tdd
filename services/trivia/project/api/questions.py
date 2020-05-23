from flask import Blueprint, request
from flask_restx import Resource, Api
from project.api.models import Question

questions_blueprint = Blueprint("questions", __name__)
api = Api(questions_blueprint)


class Questions(Resource):
    def get(self):
        page = int(request.args.get("page"))

        per_page = Question.max_results_per_page

        query = Question.query.paginate(page, per_page, False)
        questions = [item.format() for item in query.items]

        return questions, 200


api.add_resource(Questions, "/questions")
