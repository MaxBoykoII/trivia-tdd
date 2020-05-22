from unittest import TestCase
import os
from project import app


class TestConfig(TestCase):
    def setUp(self):
        """Define test variables and initialize app"""
        self.test_app = app

    def test_development_config(self):
        test_app = self.test_app

        test_app.config.from_object("project.config.DevelopmentConfig")
        assert test_app.config["SECRET_KEY"] == "MY_SECRET"
        assert not test_app.config["TESTING"]
        assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
            "DATABASE_URL"
        )

    def test_testing_config(self):
        test_app = self.test_app

        test_app.config.from_object("project.config.TestingConfig")
        assert test_app.config["SECRET_KEY"] == "MY_SECRET"
        assert test_app.config["TESTING"]
        assert not test_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
        assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
            "DATABASE_TEST_URL"
        )

    def test_production_config(self):
        test_app = self.test_app

        test_app.config.from_object("project.config.ProductionConfig")
        assert test_app.config["SECRET_KEY"] == "MY_SECRET"
        assert not test_app.config["TESTING"]
        assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
            "DATABASE_URL"
        )
