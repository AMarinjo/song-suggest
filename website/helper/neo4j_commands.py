"""
SongSuggest Flask Application
Flask Application Postgres Create, creates and populates the neo4j songs table
GROUP 12 Project
"""


def create_nodes(csv_file_path):
    """Simple method that returns the necessary commands for creating the appropriate
    nodes for the dataset used within the project

    Args:
        csv_file_path (str): String containing the csv file path
    """

    song_nodes = f"""
        LOAD CSV WITH HEADERS FROM 'file:///{csv_file_path}' AS row
        MERGE (s:Song {{
            id: toInteger(row.id),
            track_id: row.track_id,
            artists: row.artists,
            album_name: row.album_name,
            track_name: row.track_name,
            popularity: toInteger(row.popularity),
            duration_ms: toInteger(row.duration_ms),
            explicit: row.explicit = 'True',
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
        }}) WITH s, row
        RETURN COUNT(s)
        """
    print(song_nodes)
    return song_nodes


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
