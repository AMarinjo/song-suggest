"""
SongSuggest Flask Application
Flask Application views, defines different views possible when running application
GROUP 12 Project
"""
from flask import Blueprint, render_template, request, flash, jsonify
from .models import PostgresModel
from .models import Neo4jModel

views = Blueprint("views", __name__)


@views.route("/")
def homepage():
    """Used for defining home page of application

    Returns:
        Render of home.html template
    """
    return render_template("home.html")


@views.route("/search", methods=["GET", "POST"])
def search():
    """Used for searching the database. Searches postgres database specifically

    Returns:
        Render of the search template
    """
    if request.method == "POST":
        query = request.form.get("query")

        if query:
            postgres = PostgresModel()
            results = postgres.find_list(query)
            postgres.close()
            return render_template("find.html", results=results, query=query)

        return render_template("home.html")

    query = request.args.get("query")

    if query:
        postgres = PostgresModel()
        results = postgres.search(query)
        postgres.close()

        suggestions = [
            {
                "track_id": result[0],
                "track_name": result[1],
                "redirect_url": f"/redirect/{result[0]}",
            }
            for result in results
        ]
        return jsonify({"suggestions": suggestions})


@views.route("/redirect/<suggestion>")
def redirect_page(suggestion):
    """Render a page based on the selected suggestion.

    Args:
        suggestion (str): The selected suggestion.
    Returns:
        Render of a template specific to the selected suggestion.
    """
    postgres = PostgresModel()
    results_post = postgres.find_by_id(suggestion)
    postgres.close()
    print(results_post)

    neo = Neo4jModel()
    results_neo = neo.recommendations(suggestion)
    neo.close()  

    return render_template(f"profile.html", results_post=results_post[0], results_neo=results_neo)
