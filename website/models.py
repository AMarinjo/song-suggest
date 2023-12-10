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

    def recommendations(self, id):
        """Method for finding recommendation by running Neo query

        Args:
            id (str): Id searched for in database
        """
        with self.driver.session() as session:
            result = session.run(recommendations(id))
            result_data = list(result.data())
            return result_data

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
        try:
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

                cursor.execute(update_artists(table_name))

                self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if cursor is not None:
                cursor.close()

    def search(self, search_value, table_name="songs"):
        """Method for searching the postgres database

        Args:
            search_value (str, optional): Value searched for in application
            table_name (str, optional): The name of the table created. Defaults
            to "songs".
        """
        results = ""

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                search_query(table_name),
                (
                    "%" + search_value + "%",
                    "%" + search_value + "%",
                    search_value,
                    search_value,
                ),
            )
            results = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if cursor is not None:
                cursor.close()

        return results

    def find_list(self, search_value, table_name="songs"):
        """Method for searching the postgres database

        Args:
            search_value (str, optional): Value searched for in application
            table_name (str, optional): The name of the table created. Defaults
            to "songs".
        """
        results = ""

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                find_list_query(table_name),
                (
                    "%" + search_value + "%",
                    "%" + search_value + "%",
                    search_value,
                    search_value,
                ),
            )
            results = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if cursor is not None:
                cursor.close()

        return results

    def find_by_id(self, id, table_name="songs"):
        """Method for searching the postgres database

        Args:
            id (str): Id searched for in database
            table_name (str, optional): The name of the table created. Defaults
            to "songs".
        """
        result = []

        try:
            cursor = self.connection.cursor()

            cursor.execute(find_by_id(table_name, id))
            query_result = cursor.fetchall()
            temp = query_result[0]

            result.append(temp[0])  # track_id
            result.append(temp[1])  # track_name
            result.append(temp[2])  # artists
            result.append(temp[3])  # album_name
            result.append(temp[4])  # track_genre
            result.append(color_code_popularity(temp[5]))  # popularity
            min, sec = divmod(temp[6] / 1000, 60)
            min, sec = int(min), int(sec)
            result.append(min)  # duration_minutes
            result.append(sec)  # duration_remaining_seconds
            if temp[7]:  # explicit?
                result.append("Yes")
            else:
                result.append("No")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if cursor is not None:
                cursor.close()

        return result

    def find_recommendations(self, id, table_name="songs"):
        """Method for searching the postgres database and finding the recommendations

        Args:
            id (str): Id searched for in database
            table_name (str, optional): The name of the table created. Defaults
            to "songs".
        """
        result = ""

        try:
            cursor = self.connection.cursor()

            cursor.execute(find_recommendations(table_name, id))
            result = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if cursor is not None:
                cursor.close()

        return result

    def find_by_artist(self, id, artist, table_name="songs"):
        """Method for searching the postgres database by artist

        Args:
            id (str): Id searched for in database
            artist (str): Artist name to be searched for in database
            table_name (str, optional): The name of the table created. Defaults
            to "songs".
        """
        result = []

        try:
            cursor = self.connection.cursor()

            cursor.execute(find_by_artist(table_name, id, artist))
            result = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if cursor is not None:
                cursor.close()

        return result

    def tempo_search(self, danceability, liveness, table_name="songs"):
        """Searches the tempo within the database. Unlikely to be used in application.

        Args:
            table_name (str, optional): The name of the table created. Defaults
            to "songs".
            danceability (int): Danceability one might be looking for
            liveness (int): Liveness one might need to be looking for
        """
        results = ""

        try:
            cursor = self.connection.cursor()

            cursor.execute(tempo(table_name, danceability, liveness))
            results = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if cursor is not None:
                cursor.close()

        return results

    def close(self):
        """Closes the Postgres database connection"""
        self.connection.close()
