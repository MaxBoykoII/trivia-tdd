from flask import Blueprint
from flask_restx import Api, Resource
from project.api.models import Category

categories_blueprint = Blueprint("categories", __name__)
api = Api(categories_blueprint)


class Categories(Resource):
    def get(self):
        category_query = Category.query.all()
        categories = {item.id: item.type.lower() for item in category_query}

        payload = {"categories": categories}

        return payload, 200


api.add_resource(Categories, "/categories")
