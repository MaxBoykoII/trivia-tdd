import os
from unittest import TestCase

from project import create_app


class TestConfig(TestCase):
    def setUp(self):
        """Define test variables and initialize app"""
        self.test_app = create_app()
        self.test_app.config.from_object("project.config.TestingConfig")

    def test_development_config(self):
        test_app = self.test_app

        test_app.config.from_object("project.config.DevelopmentConfig")
        self.assertEqual(test_app.config["SECRET_KEY"], "MY_SECRET")
        self.assertFalse(test_app.config["TESTING"])
        self.assertEqual(
            test_app.config["SQLALCHEMY_DATABASE_URI"], os.environ.get("DATABASE_URL")
        )

    def test_testing_config(self):
        test_app = self.test_app

        test_app.config.from_object("project.config.TestingConfig")
        self.assertEqual(test_app.config["SECRET_KEY"], "MY_SECRET")
        self.assertTrue(test_app.config["TESTING"])
        self.assertFalse(test_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"])
        self.assertEqual(
            test_app.config["SQLALCHEMY_DATABASE_URI"],
            os.environ.get("DATABASE_TEST_URL"),
        )

    def test_production_config(self):
        test_app = self.test_app

        test_app.config.from_object("project.config.ProductionConfig")
        self.assertEqual(test_app.config["SECRET_KEY"], "MY_SECRET")
        self.assertFalse(test_app.config["TESTING"])
        self.assertEqual(
            test_app.config["SQLALCHEMY_DATABASE_URI"], os.environ.get("DATABASE_URL")
        )
