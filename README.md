# SongSuggest
This is a repository used for the Modern Databases project. It's a small project 
whose main purpose is to use 2 different databases with a dataset of songs in 
order to query and analyze said dataset.

## Setup & Installation
Make sure you have the latest version of Python installed.

```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

## Postgres Setup
Make sure you set up the credentials.txt and database.ini files locally to 
connect to your Postgres database. By looking at these files you will see the 
username and password need to be entered to login into the database correctly.
Likewise, make sure you have access to the database before running the 
application.

To set these files up please create the following:

- credentials.txt
- database.ini

Both files need to be created in the website/helper directories.

The database.ini file needs to look as follows:

```bash
[postgresql]
host=s-l112.engr.uiowa.edu
database=mdb_studentxx
user=mdb_studentxx
password=password123
```

The credential.txt file needs to look as follows:

```bash
mdb_studentxx
password123
```

## Neo4j Setup
For the Neo4j setup, ensure you have created a database to work with while also
grabbing the .csv file from the project and adding it to the import folder of the
Neo4j database. 

Follow this link [here](https://neo4j.com/developer/desktop-csv-import/) for more information.

## Running The App
```bash
python main.py
```

## Viewing The App
Go to `http://127.0.0.1:8001`

## Improvements
Consider running these two commands in your Postgres database to potentially improve the 
search performance:

```bash
CREATE INDEX idx_artists_trgm ON songs USING GIN (artists gin_trgm_ops)
```

```bash
CREATE INDEX idx_track_name_trgm ON songs USING GIN (track_name gin_trgm_ops)
```

```bash
CREATE INDEX idx_acousticness ON songs USING btree (acousticness)
```

```bash
CREATE INDEX idx_danceability ON songs USING btree (danceability)
```

```bash
CREATE INDEX idx_liveness ON songs USING btree (liveness)
```

```bash
CREATE INDEX idx_songid ON songs USING btree (track_id)
```

Consider modifying the dataset manually. For some reason, the dataset imported comes
with duplicate entries. Run the below-shown commands to remove the duplicate entries.

```bash
CREATE TABLE temp AS
SELECT DISTINCT ON (track_id) * FROM songs;

DROP TABLE songs;

ALTER TABLE temp RENAME TO songs;
```
