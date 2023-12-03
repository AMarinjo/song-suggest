"""
SongSuggest Flask Application 
Using create app method from website. This import and sets up the Flask application
GROUP 12 Project
"""

from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
