from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# instantiate the db
db = SQLAlchemy()

cors = CORS()

# application factory pattern
def create_app(script_info=None):

    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})

    # register blueprints
    from project.api.ping import ping_blueprint
    from project.api.questions import questions_blueprint

    app.register_blueprint(ping_blueprint)
    app.register_blueprint(questions_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
