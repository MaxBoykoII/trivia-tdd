from flask import Flask, jsonify
from flask_restx import Resource, Api
import os

# instantiate app
app = Flask(__name__)

api = Api(app)

# set config
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object("project.config.DevelopmentConfig")


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


api.add_resource(Ping, "/ping")
