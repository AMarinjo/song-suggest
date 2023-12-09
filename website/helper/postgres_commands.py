"""
SongSuggest Flask Application
Flask Application Postgres Create, creates and populates the postgres songs table
GROUP 12 Project
"""


def create_table(table_name):
    """Simple method that returns the necessary commands for creating the appropriate
    table for the dataset used within the project

    Args:
        table_name (str): Table name used within database
    """

    table_schema = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        track_id VARCHAR(50),
        artists TEXT,
        album_name TEXT,
        track_name TEXT,
        popularity INT,
        duration_ms INT,
        explicit BOOLEAN,
        danceability NUMERIC,
        energy NUMERIC,
        key INT,
        loudness NUMERIC,
        mode INT,
        speechiness NUMERIC,
        acousticness NUMERIC,
        instrumentalness NUMERIC,
        liveness NUMERIC,
        valence NUMERIC,
        tempo NUMERIC,
        time_signature INT,
        track_genre VARCHAR(50)
    )
    """

    return table_schema


def check_table_available(table_name):
    """Simple method to check whether or not the table being added is available or not

    Args:
        table_name (str): Table name used within database
    """

    table_available = f"""
    SELECT EXISTS (SELECT 1 FROM information_schema.tables 
    WHERE table_name = '{table_name}')
    """

    return table_available

