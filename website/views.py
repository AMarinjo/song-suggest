"""
SongSuggest Flask Application
Flask Application views, defines different views possible when running application
GROUP 12 Project
"""
from flask import Blueprint, render_template, request, flash, jsonify

views = Blueprint("views", __name__)


@views.route("/")
def homepage():
    """Used for defining home page of application

    Returns:
        Render of home.html template
    """
    return render_template("home.html")
