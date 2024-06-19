import psycopg2
from os import environ  # Gives the program access to the environment variables
from dotenv import load_dotenv  # Loads variables from a file into the environment
import sys

DEBUG = True


def load_dotenv_vars():

    if DEBUG is True:
        load_dotenv('.env.local')
    else:
        load_dotenv('.env.prod')


def get_connection():

    imported_username = environ.get("DATABASE_USERNAME")
    imported_password = environ.get("DATABASE_PASSWORD")
    imported_host_ip = environ.get("DATABASE_IP")
    imported_port = environ.get("DATABASE_PORT")
    imported_database_name = environ.get("DATABASE_NAME")

    connection = psycopg2.connect(
        user=imported_username,
        password=imported_password,
        host=imported_host_ip,
        port=imported_port,
        database=imported_database_name
    )

    return connection


if __name__ == "__main__":
    load_dotenv_vars()
    conn = get_connection()
    print(conn)
    conn.close()
