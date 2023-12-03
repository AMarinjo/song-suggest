"""
SongSuggest Flask Application
Flask Application postgres config, used to configure Postgres database model
GROUP 12 Project
"""

from configparser import ConfigParser
import os


def config(filename="database.ini", section="postgresql"):
    """Configure a database

    Args:
        filename (str, optional): Filename used to configure database. Defaults
        to "database.ini".
        section (str, optional): Section used to obtain specific section of
        database.ini file. Defaults to "postgresql".

    Raises:
        File not found excpetion

    Returns:
        Parses file and returns configuration files
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = base_dir + "\\helper\\" + filename

    parser = ConfigParser()
    # read config file
    parser.read(file_path)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {file_path} file")

    return db


def credentials(filename="credentials.txt"):
    """Parse the credentials.txt file"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = base_dir + "\\helper\\" + filename

    with open(file_path, "r") as file:
        username = file.readline().strip()
        password = file.readline().strip()

    return username, password
