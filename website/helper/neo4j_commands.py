"""
SongSuggest Flask Application
Flask Application Postgres Create, creates and populates the neo4j songs table
GROUP 12 Project
"""


def create_song(csv_file_path):
    """Simple method that returns the necessary commands for creating the appropriate
    nodes for the dataset used within the project

    Args:
        csv_file_path (str): String containing the csv file path
    """

    song = f"""
        LOAD CSV WITH HEADERS FROM 'file:///{csv_file_path}' AS row
        CREATE (s:Song {{
            id: toInteger(row.id),
            track_id: row.track_id,
            artists: row.artists,
            album_name: row.album_name,
            track_name: row.track_name,
            popularity: toInteger(row.popularity),
            duration_ms: toInteger(row.duration_ms),
            explicit: toBoolean(row.explicit),
            danceability: toFloat(row.danceability),
            energy: toFloat(row.energy),
            key: toInteger(row.key),
            loudness: toFloat(row.loudness),
            mode: toInteger(row.mode),
            speechiness: toFloat(row.speechiness),
            acousticness: toFloat(row.acousticness),
            instrumentalness: toFloat(row.instrumentalness),
            liveness: toFloat(row.liveness),
            valence: toFloat(row.valence),
            tempo: toFloat(row.tempo),
            time_signature: toInteger(row.time_signature),
            track_genre: row.track_genre
        }})
        """

    return song


def create_artist(csv_file_path):
    """Simple method that returns the necessary commands for creating the appropriate
    nodes for the dataset used within the project

    Args:
        csv_file_path (str): String containing the csv file path
    """

    artist = f"""
        LOAD CSV WITH HEADERS FROM 'file:///{csv_file_path}' AS row
        UNWIND split(row.artists,';') AS artist
        WITH DISTINCT artist
        CREATE (:Artist {{name:artist}})
        """

    return artist


def create_album(csv_file_path):
    """Simple method that returns the necessary commands for creating the appropriate
    nodes for the dataset used within the project

    Args:
        csv_file_path (str): String containing the csv file path
    """

    album = f"""
        LOAD CSV WITH HEADERS FROM 'file:///{csv_file_path}' AS row
        UNWIND row.album_name AS album
        WITH DISTINCT album
        CREATE (:Album {{name:album}})
        """

    return album


def create_genre(csv_file_path):
    """Simple method that returns the necessary commands for creating the appropriate
    nodes for the dataset used within the project

    Args:
        csv_file_path (str): String containing the csv file path
    """

    genre = f"""
        LOAD CSV WITH HEADERS FROM 'file:///{csv_file_path}' AS row
        UNWIND row.track_genre AS genre
        WITH DISTINCT genre
        CREATE (:Genre {{name:genre}})
        """

    return genre


def create_artist_album():
    """Simple method that returns the necessary commands for creating the appropriate
    relations for the dataset used within the project
    """

    artist_album = """
        MATCH (song: Song)
        MATCH (artists: Artist {name: song.artists})
        MATCH (album: Album {name: song.album_name})
        CREATE (artists)-[:ARTIST_MADE_ALBUM]->(album)
        """

    return artist_album


def create_artist_song():
    """Simple method that returns the necessary commands for creating the appropriate
    relations for the dataset used within the project
    """

    artist_song = """
        MATCH (song: Song)
        MATCH (album: Album {name: song.album_name})
        CREATE (album)-[:ALBUM_HAS_TRACK]->(song)
        """

    return artist_song


def create_song_genre():
    """Simple method that returns the necessary commands for creating the appropriate
    relations for the dataset used within the project
    """

    song_genre = """
        MATCH (song: Song)
        MATCH (genre: Genre {name: song.track_genre})
        CREATE (song)-[:IN_GENRE]->(genre)
        """

    return song_genre


def check_node_available(label, neo_property):
    """Simple method to check whether or not the node being added is available
    or not

    Args:
        label (str): Description of label used within database
        neo_property (str): Property of neo database

    Returns:
        Neo4j command needed to check whether node is available or not within
        database
    """

    table_available = (
        f"MATCH (n:{label} {{{neo_property}: $value}}) RETURN COUNT(n) AS count"
    )

    return table_available

def recs(song):
    """
    
    """