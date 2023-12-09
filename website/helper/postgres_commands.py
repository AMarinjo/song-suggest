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


def update_artists(table_name):
    """Simple method that updates the artists column and changes the semicolumns
    into commas within the string

    Args:
        table_name (str): Table name used within database
    """

    update_query = f"""
    UPDATE {table_name}
    SET artists = REPLACE(artists, ';', ', ')
    """

    return update_query


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


def search_query(table_name):
    """Simple method to search database

    Args:
        table_name (str): Table name used within database
    """

    search = f"""
        SELECT track_id, track_name || ' - ' || artists AS track_and_artists
        FROM {table_name} 
        WHERE track_name ILIKE %s OR artists ILIKE %s
        ORDER BY 
            similarity(track_name, %s) + similarity(artists, %s) DESC
        LIMIT 20
    """

    return search


def find_list_query(table_name):
    """Simple method to search database

    Args:
        table_name (str): Table name used within database
    """

    find_list = f"""
        SELECT track_id, track_name || ' - ' || artists AS track_and_artists, album_name, track_genre 
        FROM {table_name} 
        WHERE track_name ILIKE %s OR artists ILIKE %s
        ORDER BY 
            similarity(track_name, %s) + similarity(artists, %s) DESC
        LIMIT 50
    """

    return find_list


def find_by_id(table_name, search_id):
    """Simple method to search database by id

    Args:
        table_name (str): Table name used within database
        search_id (str): Id that needs to be searched by
    """

    search_query = f"""
        SELECT track_id, track_name, artists, album_name, track_genre 
        FROM {table_name} 
        WHERE track_id = '{search_id}'
    """

    return search_query


def tempo(table_name, danceability, liveness):
    """Find specific type of tempo and songs

    Args:
        table_name (str): Table name used within database
        danceability (int): Danceability one might be looking for
        liveness (int): Liveness one might need to be looking for
    """

    tempo = f"SELECT track_name FROM {table_name} ORDER BY ABS(danceability"
    tempo += f" {danceability}) + ABS(liveness-{liveness}) LIMIT 5;"

    return tempo
