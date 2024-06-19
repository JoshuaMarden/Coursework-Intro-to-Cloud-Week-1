from typing import Any
import psycopg2
import json
from psycopg2.extensions import connection, cursor
from datetime import datetime, date


def get_connection() -> connection:
    conn = psycopg2.connect("dbname=lmdb user=joshuasigma host=localhost")
    return conn


def get_cursor(conn: connection) -> cursor:
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return cur


def get_movies(search: str = None, sort_by: str = None, sort_order: str = None) -> list[dict]:
    # Example implementation
    conn = get_connection()
    cursor = get_cursor(conn)

    default_sort_by = 'names'
    default_sort_order = 'desc'

    valid_sort_by_columns = ['names', 'release_date',
                             'country', 'other_valid_columns']
    valid_sort_orders = ['asc', 'desc']

    base_query = """
        SELECT *
        FROM movie
        JOIN original_language ON original_language.language_id = movie.original_language_id
        JOIN release_date ON release_date.date_id = movie.release_date_id
        JOIN country ON country.country_id = movie.country_id
    """

    # Validate and set sort_by and sort_order
    if sort_by not in valid_sort_by_columns:
        sort_by = default_sort_by

    if sort_order not in valid_sort_orders:
        sort_order = default_sort_order

    search_parameters = []
    if search:
        base_query += " WHERE movie.names LIKE %s OR movie.description LIKE %s"
        search_parameters.extend([f"%{search}%", f"%{search}%"])

    base_query += f" ORDER BY {sort_by} {sort_order}"

    cursor.execute(base_query, search_parameters)
    rows = cursor.fetchall()

    cursor.execute("SELECT movie_id, genre_id FROM movie_genre_assignment")
    assignments = cursor.fetchall()

    cursor.execute("SELECT genre_id, genre_type FROM genre")
    genres = cursor.fetchall()

    conn.close()
    cursor.close()

    for movie_dict in rows:
        movie_id = movie_dict["movie_id"]

        genres_with_id_match = []
        for genre_assignment in assignments:
            if genre_assignment["movie_id"] == movie_id:
                genres_with_id_match.append(genre_assignment["genre_id"])

        genre_types = []
        for genre in genres:
            if genre["genre_id"] in genres_with_id_match:
                genre_types.append(genre["genre_type"])

        genre_types = ", ".join(genre_types)

        movie_dict["genres"] = genre_types
        del movie_dict["genre_id"]

    return rows


def get_movie_by_id(movie_id: int) -> dict[str, Any]:
    conn = get_connection()
    cursor = get_cursor(conn)

    base_query = """
    SELECT *
    FROM movie
    WHERE movie.movie_id = %s
    """

    search_parameter = [movie_id]
    cursor.execute(base_query, search_parameter)

    row = cursor.fetchone()

    conn.close()
    cursor.close()

    return row


def create_movie(title: str, release_date: date, genre: str, overview: str, status: str, budget: int, revenue: int, country: str, language: str) -> dict:
    ...
    return False


def update_movie(title: str, release_date: date, genre: str, overview: str, status: str, budget: int, revenue: int, country: str, language: str) -> dict[str, Any]:
    ...
    return False


def delete_movie(movie_id: int) -> bool:
    ...
    return False


def get_genres() -> list[dict[str, str]]:
    ...
    return False


def get_genre(genre_id: int) -> dict:
    ...
    return False


def get_movies_by_genre(genre_id: int) -> list[dict[str, Any]]:
    ...
    return False


def get_movie_by_country(country_code, sort_by: str = None, sort_order: str = None) -> list[dict]:
    ...
    return False


def get_countries() -> list[str]:
    ...
    return []
