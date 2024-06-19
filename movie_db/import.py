"""A script to import all of the movies in imdb_movies.csv into the database"""

"""
Don't forget to run:
`psql -d lmdb -a -f schema.sql`

Connect to production
`psql -h <hostname> -p <port> -U <username> -d <database>`

There are a lot of nested inserts. VERY inefficient.
"""


###
from psycopg2 import extras # must specify this import. Not sure why.
import psycopg2
import csv
from db_connect import get_connection, load_dotenv_vars
load_dotenv_vars()
conn = get_connection()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def load_csv(movies_csv: str) -> list[dict]:
    """Loads csv file, returns it as a list of dicts"""
    with open(movies_csv, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def get_genres_and_fill_genre_table(movies: list[dict]) -> None:
    """Get all possible genres and populate genre table"""
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


def get_languages_and_fill_language_table(movies: list[dict]) -> None:
    """Get all possible genres and populate genre table"""

    all_languages_categories = set()

    for movie in movies:
        movie_language = movie.get("orig_lang")
        all_languages_categories.add(movie_language)

    for language in all_languages_categories:
        cur.execute(
            "INSERT INTO original_language(original_language)\
            VALUES (%s)",
            (language,)
        )


def get_release_dates_and_fill_release_date_table(movies: list[dict]) -> None:
    """Get all possible genres and populate genre table"""

    all_dates = set()

    for movie in movies:
        date = movie.get("date_x")
        all_dates.add(date)

    for date in all_dates:
        cur.execute(
            "INSERT INTO release_date(release_date)\
            VALUES (%s)",
            (date,)
        )


def get_countries_and_fill_country_table(movies: list[dict]) -> None:
    """Get all possible genres and populate genre table"""

    all_countries = set()

    for movie in movies:
        country = movie.get("country")
        all_countries.add(country)

    for country in all_countries:
        cur.execute(
            "INSERT INTO country(country)\
            VALUES (%s)",
            (country,)
        )


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
    return current_movie_id


def import_language_into_language_and_movie_tables(movie: dict, movie_id) -> None:
    """Takes the movie language, adds it to language table,
    adds language_id to movie table"""
    column_value = movie.get("country")
    cur.execute("""
                UPDATE movie
                SET country_id = (
                    SELECT country_id
                    FROM country
                    WHERE country.country = %s
                )
                WHERE movie.movie_id = %s;
            """, (column_value, movie_id,))


def import_date_into_movie_and_date_tables(movie: dict, movie_id) -> None:
    """Takes the movie date, adds it to date table,
    adds date_id to movie table"""
    column_value = movie.get("date_x")
    cur.execute("""
                UPDATE movie
                SET release_date_id = (
                    SELECT date_id
                    FROM release_date
                    WHERE release_date.release_date = %s
                )
                WHERE movie.movie_id = %s;
            """, (column_value, movie_id,))


def import_country_into_country_and_movie_tables(movie: dict, movie_id) -> None:
    """Takes the movie country, adds it to country table,
    adds country_id to movie table"""

    column_value = movie.get("orig_lang")
    cur.execute("""
                UPDATE movie
                SET original_language_id = (
                    SELECT language_id
                    FROM original_language
                    WHERE original_language.original_language = %s
                )
                WHERE movie.movie_id = %s;
            """, (column_value, movie_id,))


def import_genre_and_link_via_assignment_table(movie: dict, movie_id) -> None:
    """Takes movie genres, finds genre_id in genre table, links genre to movie
    via an id in move_genre_assignment, adds id to movie table"""

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


def import_movies_to_database(movies: list[dict]) -> None:
    """imports movies from local csv to local database"""

    get_genres_and_fill_genre_table(movies)
    get_countries_and_fill_country_table(movies)
    get_languages_and_fill_language_table(movies)
    get_release_dates_and_fill_release_date_table(movies)

    for movie_dict in movies:

        movie_name = movie_dict.get('names')
        print(f"Uploading data for: {movie_name}")

        current_movie_id = import_movie_straight_to_movie_table(movie_dict)

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


if __name__ == "__main__":
    cur = conn.cursor()
    movies = load_csv("imdb_movies.csv")
    import_movies_to_database(movies)
    conn.commit()
    cur.close()
    conn.close()
