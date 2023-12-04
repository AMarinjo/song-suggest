"""
SongSuggest Flask Application
Initialize Flask Application by running the create app function seen below
GROUP 12 Project
"""

from flask import Flask
from .views import views
from .models import PostgresModel, Neo4jModel


def create_app():
    """Create web application to be used. Called from main.py

    Returns:
        Returns application object
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "This is super secret.."

    app.register_blueprint(views, url_prefix="/")

    postgres = PostgresModel()
    neo4j = Neo4jModel()

    postgres.create_table()
    neo4j.create_table()

    return app
