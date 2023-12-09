"""
SongSuggest Flask Application
Flask Application models, sets up the database models for the application
GROUP 12 Project
"""

import os
from urllib.parse import quote
import psycopg2
from psycopg2 import sql
from neo4j import GraphDatabase
from .helper.postgres_commands import *
from .helper.postgres_config import config, credentials
from .helper.neo4j_commands import *


class Neo4jModel:
    """
    Neo4jModel class, addressed Neo4j commands needed within application
    """

    def __init__(
        self, url="bolt://localhost:7687", username="neo4j", password="password"
    ):
        """Initializes the Neo4j object

        Args:
            url (str, optional): The localhost address of the Neo4j database.
            Defaults to "bolt://localhost:7687".
            username (str, optional): Username of the database that needs to be
            connected to. Defaults to "neo4j".
            password (str, optional): Password of the database that needs to be
            connected to. Defaults to "password".
        """
        self.url = url
        self.driver = GraphDatabase.driver(url, auth=(username, password))

    def create_table(self, csv_file="dataset.csv"):
        """Creates and populates the neo4j with the included .csv file

        Args:
            csv_file_path (str, optional): The .csv file path for dataset used.
            Defaults to "dataset.csv".
        """
        comparison_value = "210JCw2LbYD4YIs8GiZ9iP"

        with self.driver.session() as session:
            result = session.run(
                check_node_available("Song", "track_id"), value=comparison_value
            )
            node_count = result.single()["count"]

        if node_count > 0:
            print(
                f""" * Value {comparison_value} already exists in Neo4j database. """
                + """Data already imported."""
            )
        else:
            with self.driver.session() as session:
                session.run(create_song(csv_file))
                session.run(create_artist(csv_file))
                session.run(create_album(csv_file))
                session.run(create_genre(csv_file))
                session.run(create_artist_album())
                session.run(create_artist_song())
                session.run(create_song_genre())

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

    def create_table(self, table_name="songs", csv_file="dataset.csv"):
        """Creates and populates the postgres with the included .csv file

        Args:
            table_name (str, optional): The name of the table created. Defaults
            to "songs".
            csv_file_path (str, optional): The .csv file path for dataset used.
            Defaults to "dataset.csv".
        """
        cursor = self.connection.cursor()
        cursor.execute(check_table_available(table_name))
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print(f" * Table {table_name} already exists in Postgres database.")
        else:
            cursor.execute(create_table(table_name))
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_file_path = base_dir + "\\website\\helper\\" + csv_file

            with open(csv_file_path, "r", encoding="utf-8") as file:
                cursor.copy_expert(
                    f"COPY {table_name} FROM STDIN WITH CSV HEADER", file
                )

            self.connection.commit()

        cursor.close()

    def search(self, search_value):
        """Method for searching the postgres database

        Args:
            search_value (str, optional): Value searched for in application
        """
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT track_name, artists, album_name FROM songs WHERE track_name ILIKE %s",
            ("%" + search_value + "%",),
        )
        results = cursor.fetchall()
        cursor.close()

        return results
    
    def close(self):
        """Closes the Postgres database connection"""
        self.connection.close()
