from flask import Flask, current_app, jsonify, request
from psycopg2 import extras
from datetime import datetime, date
from typing import Any
from database import get_movies, get_movie_by_id, create_movie, update_movie, delete_movie, get_genres, get_genre, get_movies_by_genre, get_movie_by_country, get_countries


"""
Note from the Movie DB API team:
 - This half-finished code was written by an intern with no coding experience so expect there to be bugs and issues.
 - Please review the code and make any necessary changes to ensure it is production-ready. Good luck!
"""

app = Flask(__name__)
app.json.sort_keys = False


def validate_sort_by(sort_by: str) -> bool:
    if sort_by and sort_by not in ["title", "release_date", "genre", "revenue", "budget", "score"]:
        return False

    return True


def validate_sort_order(sort_order: str) -> bool:
    if sort_order and sort_order not in ["asc", "desc"]:
        return False

    return True


@app.route("/", methods=["GET"])
def endpoint_index():
    return jsonify({"message": "Welcome to the Movie API"})


@app.route("/movies", methods=["GET", "POST"])
def endpoint_get_movies():

    if request.method == "GET":
        sort_by = request.args.get("sort_by")
        sort_order = request.args.get("sort_order")
        search = request.args.get("search")

        if not validate_sort_by(sort_by):
            return jsonify({"error": "Invalid sort_by parameter"}), 400

        if not validate_sort_order(sort_order):
            return jsonify({"error": "Invalid sort_order parameter"}), 400

        movies = get_movies(search, sort_by, sort_order)

        if not movies:
            return jsonify({"error": "No movies found"}), 404

        return jsonify(movies), 200

    elif request.method == "POST":
        data = request.json
        title = data["title"]
        release_date = data["release_date"]
        genre = data["genre"]
        actors = data.get("actors", [])
        overview: str = data.get("overview", "")
        status = data.get("status", "released")
        budget: int = data.get("budget", 0)
        revenue: int = data.get("revenue", 0)
        country: str = data.get("country")
        language: str = data.get("language")

        if not title or not release_date or not genre or not country or not language or not actors:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            datetime.strptime(release_date, "%m/%d/%Y")
        except ValueError:
            return jsonify({"error": "Invalid release_date format. Please use MM/DD/YYYY"}), 400

        try:
            movie = create_movie(title, release_date, genre, actors,
                                 overview, status, budget, revenue, country, language)
            return jsonify({'success': True, "movie": movie}), 201
        except Exception as e:

            return jsonify({"error": str(e)}), 500
    return jsonify({"error": True,
                    "message": "method not allowed ฅ^•ﻌ•^ฅ "}), 405


@app.route("/movies/<int:movie_id>", methods=["GET", "PATCH", "DELETE"])
def endpoint_get_movie(movie_id: int):

    if request.method == "PATCH":
        data = request.json
        title = data.get("title")
        release_date = data.get("release_date")
        genre = data.get("genre")
        overview = data.get("overview")
        status = data.get("status")
        budget = data.get("budget")
        revenue = data.get("revenue")
        country = data.get("country")
        language = data.get("language")

        if not title and not release_date and not genre and not overview and not status and not budget and not revenue and not country and not language:
            return jsonify({"error": "No fields to update"}), 400

        try:
            movie = update_movie(
                title, release_date, genre, overview, status, budget, revenue, country, language)
            return jsonify({'success': True, "movie": movie}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "GET":

        if isinstance(movie_id, int):
            movie = get_movie_by_id(movie_id)

        if movie:
            return jsonify(movie), 200
        else:
            return jsonify({"error": "Movie not found"}), 404

    elif request.method == "DELETE":

        success = delete_movie(movie_id)

        if not success:
            return jsonify({"error": "Movie could not be deleted"}), 404

        return jsonify({"message": "Movie deleted"})

    if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
