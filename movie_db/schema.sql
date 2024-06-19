-- This file contains all of the SQL commands to create the database, tables and relationships for the Movies Database

DROP TABLE IF EXISTS movie CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS movie_genre_assignment CASCADE;
DROP TABLE IF EXISTS release_date CASCADE;
DROP TABLE IF EXISTS original_language CASCADE;
DROP TABLE IF EXISTS country CASCADE;


CREATE TABLE
    movie (
        movie_id INT GENERATED ALWAYS AS IDENTITY,
        names TEXT,
        release_date_id INT,
        genre_id SMALLINT,
        score FLOAT,
        synopsis TEXT,
        original_title TEXT,
        release_status TEXT,
        original_language_id SMALLINT,
        budget BIGINT,
        revenue BIGINT,
        country_id SMALLINT,
        PRIMARY KEY (movie_id)
    );

CREATE TABLE
    genre(
        genre_id SMALLINT GENERATED ALWAYS AS IDENTITY,
        genre_type text NOT NULL,
        PRIMARY KEY (genre_id)
    );

CREATE TABLE 
    movie_genre_assignment(
        movie_genre_assignment_id INT GENERATED ALWAYS AS IDENTITY,
        movie_id INT NOT NULL,
        genre_id SMALLINT NOT NULL,
        PRIMARY KEY (movie_genre_assignment_id),
        FOREIGN KEY (movie_id) REFERENCES movie (movie_id),
        FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
    );

CREATE TABLE
    release_date(
        date_id INT GENERATED ALWAYS AS IDENTITY,
        release_date DATE NOT NULL,
        PRIMARY KEY (date_id)
    );

CREATE TABLE
    original_language(
      language_id  SMALLINT GENERATED ALWAYS AS IDENTITY,
      original_language TEXT NOT NULL,
      PRIMARY KEY (language_id)
    );

CREATE TABLE
    country(
        country_id SMALLINT GENERATED ALWAYS AS IDENTITY,
        country TEXT NOT NULL,
        PRIMARY KEY (country_id)
    );



