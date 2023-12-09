"""
SongSuggest Flask Application
Flask Application views, defines different views possible when running application
GROUP 12 Project
"""
from flask import Blueprint, render_template, request, flash, jsonify
from .models import PostgresModel

views = Blueprint("views", __name__)


@views.route("/")
def homepage():
    """Used for defining home page of application

    Returns:
        Render of home.html template
    """
    return render_template("home.html")


@views.route("/search")
def search():
    """Used for searching the database. Searches postgres database specifically

    Returns:
        Render of the search template
    """
    query = request.args.get("query")

    if query:
        postgres = PostgresModel()

        results = postgres.search(query)

        postgres.close()

        return render_template("home.html", results=results, query=query)
    else:
        return render_template("home.html", message="Please enter a search query.")

@views.route("/getRecs")
def getRecs():
    """Used for giving song recommendations based on the song, artist, and album selected from the search menu. Searches Neo4j
    
    Returns:
        Render of recommendations template
    """
    song_info = request.args.get("selected_track")

    if song_info:
        info_split = song_info.split('|')
        song_name = info_split[0].strip()
        song_artist = info_split[1].strip()
        song_album = info_split[2].strip()

        recommendations = 'neo query'
        
        return render_template("home.html", recommendations=recommendations)
    else:
        return render_template("error.html",message="Invalid request.")