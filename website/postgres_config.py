"""
SongSuggest Flask Application
Flask Application postgres config, used to configure Postgres database model
GROUP 12 Project
"""

from configparser import ConfigParser


def config(filename="helper/database.ini", section="postgresql"):
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
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return db


def credentials():
    """Parse the credentials.txt file"""
    with open("helper/credentials.txt", "r") as file:
        username = file.readline().strip()
        password = file.readline().strip()

    return username, password
