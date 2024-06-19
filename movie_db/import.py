"""A script to import all of the movies in imdb_movies.csv into the database"""

"""
Don't forget to run:
`psql -d lmdb -a -f tables.sql`

Connect to production
`psql -h <hostname> -p <port> -U <username> -d <database>`


In its current state this will create duplicates in the supporting
tables, but not in movie.

TODO: populate date, country and language tables, THEN link to
      each movie. Avoid duplication. Something similar to
      what is done with genres but w/o assignment table.
"""


from psycopg2 import extras # must specify this import. Not sure why.
import psycopg2
import csv
from db_connect import get_connection
conn = get_connection()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def load_csv(movies_csv: str) -> list[dict]:
    """Loads csv file, returns it as a list of dicts"""
    with open(movies_csv, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def get_genres_and_fill_genre_table(movies: list[dict]) -> None:
    """Get all possible genres and populate genre table"""

    cur = conn.cursor()
    all_genre_categories = set()

    for movie in movies:
        movie_genres = movie.get("genre")
        movie_genres = movie_genres.split(", ")

        for genre in movie_genres:
            all_genre_categories.add(genre)

    for genre in all_genre_categories:
        cur.execute(
            "INSERT INTO genre(genre_type)\
            VALUES (%s)",
            (genre,)
        )

    conn.commit()


def import_movie_straight_to_movie_table(movie: dict) -> int:
    """movie data that goes ONLY into movie table is imported here.
    Returns the id of the movie imported."""

    csv_and_database_columns = [
        ("names", "names"),
        ("score", "score"),
        ("overview", "synopsis"),
        ("orig_title", "original_title"),
        ("status", "release_status"),
        ("budget_x", "budget"),
        ("revenue", "revenue")
    ]

    cur = conn.cursor()

    for name_pair in csv_and_database_columns:

        column_name = name_pair[1]
        column_value = movie.get(name_pair[0])

        if column_name in ["budget", "revenue", "score"]:
            column_value = float(column_value)

        elif column_value.startswith(' '):
            column_value = column_value.strip()

        if name_pair == csv_and_database_columns[0]:

            cur.execute(
                f"INSERT INTO movie ({column_name})\
                VALUES (%s)\
                RETURNING movie_id",
                (column_value,)
            )
            current_movie_id = cur.fetchone()[0]

        else:
            cur.execute(
                f"UPDATE movie\
                SET {column_name} = (%s)\
                WHERE movie_id = %s",
                (column_value, current_movie_id)
            )

    conn.commit()

    return current_movie_id


def import_date_into_movie_and_date_tables(movie: dict, movie_id) -> None:
    """Takes the movie date, adds it to date table,
    adds date_id to movie table"""

    cur = conn.cursor()

    column_value = movie.get("date_x")
    cur.execute(
        f"INSERT INTO release_date(release_date)\
                 VALUES (%s)\
                 RETURNING date_id",
        (column_value,)
    )
    date_id = cur.fetchone()[0]
    cur.execute(
        "UPDATE movie\
                 SET release_date_id = %s\
                 WHERE movie_id = %s",
        (date_id, movie_id)
    )

    conn.commit()


def import_language_into_language_and_movie_tables(movie: dict, movie_id) -> None:
    """Takes the movie language, adds it to language table,
    adds language_id to movie table"""

    cur = conn.cursor()

    column_value = movie.get("orig_lang")
    cur.execute(
        "INSERT INTO original_language(original_language)\
            VALUES (%s)\
            RETURNING language_id",
        (column_value,)
    )
    language_id = cur.fetchone()[0]

    cur.execute(
        "UPDATE movie\
            SET original_language_id = %s\
            WHERE movie_id = %s",
        (language_id, movie_id)
    )

    conn.commit()


def import_country_into_country_and_movie_tables(movie: dict, movie_id) -> None:
    """Takes the movie country, adds it to country table,
    adds country_id to movie table"""

    cur = conn.cursor()

    column_value = movie.get("country")
    cur.execute(
        "INSERT INTO country (country)\
            VALUES (%s)\
            RETURNING country_id",
        (column_value,)
    )
    country_id = cur.fetchone()[0]

    cur.execute(
        "UPDATE movie\
            SET country_id = %s\
            WHERE movie_id = %s",
        (country_id, movie_id)
    )

    conn.commit()


def import_genre_and_link_via_assignment_table(movie: dict, movie_id) -> None:
    """Takes movie genres, finds genre_id in genre table, links genre to movie
    via an id in move_genre_assignment, adds id to movie table"""

    cur = conn.cursor()

    movie_genres = movie.get("genre")
    movie_genres = movie_genres.split(", ")
    for genre in movie_genres:

        cur.execute(
            "SELECT genre_id\
            FROM genre\
            WHERE genre_type = %s",
            (genre,)
        )

        genre_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO movie_genre_assignment(genre_id, movie_id)\
            VALUES (%s, %s)\
            RETURNING movie_genre_assignment_id",
            (genre_id, movie_id)
        )

        movie_genre_assignment_id = cur.fetchone()[0]

        cur.execute(
            "UPDATE movie\
            SET genre_id = %s\
            WHERE movie_id = %s",
            (movie_genre_assignment_id, movie_id)
        )

    conn.commit()


def import_movies_to_database(movies: list[dict]) -> None:
    """imports movies from local csv to local database"""

    get_genres_and_fill_genre_table(movies)

    for movie_dict in movies:

        current_movie_id =\
            import_movie_straight_to_movie_table(movie_dict)

        import_date_into_movie_and_date_tables(
            movie_dict, current_movie_id)
        import_language_into_language_and_movie_tables(
            movie_dict, current_movie_id)
        import_language_into_language_and_movie_tables(
            movie_dict, current_movie_id)
        import_country_into_country_and_movie_tables(
            movie_dict, current_movie_id)
        import_genre_and_link_via_assignment_table(
            movie_dict, current_movie_id)

    cur.close()
    conn.close()


if __name__ == "__main__":
    movies = load_csv("imdb_movies.csv")
    import_movies_to_database(movies)
