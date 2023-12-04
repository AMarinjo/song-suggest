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

Make sure you set up the credentials.txt and database.ini files locally to 
connect to your Postgres database. By looking at these files you will see the 
username and password need to be entered to login into the database correctly.

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

## Running The App
```bash
python main.py
```

## Viewing The App
Go to `http://127.0.0.1:5000`
