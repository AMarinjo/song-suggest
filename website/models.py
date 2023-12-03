"""
SongSuggest Flask Application
Flask Application models, sets up the database models for the application
GROUP 12 Project
"""

import psycopg2
from neo4j import GraphDatabase
from .postgres_config import config, credentials


class Neo4jModel:
    """
    Neo4jModel class, addressed Neo4j commands needed within application
    """

    def __init__(self, url="bolt://localhost:7687", username="neo4j", password="neo4j"):
        """Initializes the Neo4j object

        Args:
            url (str, optional): The localhost address of the Neo4j database.
            Defaults to "bolt://localhost:7687".
            username (str, optional): Username of the database that needs to be
            connected to. Defaults to "neo4j".
            password (str, optional): Password of the database that needs to be
            connected to. Defaults to "neo4j".
        """
        self.url = url
        self.driver = GraphDatabase.driver(url, auth=(username, password))

    def close(self):
        """Closes the Neo4j database connection"""
        self.driver.close()


class PostgresModel:
    """
    Postgres class, addressed Postgres commands needed within application
    """

    def __init__(self):
        """Initializes the Postgres object"""
        params = config()
        params["user"], params["password"] = credentials()

        self.connection = psycopg2.connect(**params)
        self.cursor = self.connection.cursor

    def close(self):
        """Closes the Postgres database connection"""
        self.connection.close()
