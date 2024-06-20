import pytest
from flask import json
from datetime import datetime
from api import app
"""
Note from the Movie DB API team:
 - This half-finished code was written by an intern with no coding experience so expect there to be bugs and issues.
 - Lots of these tests will not work as they are - you are tasked with fixing them to work with your new database solution
 - You will notice that all of these tests connect to our *real* database. Fix them so that you mock the data correctly
"""


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_endpoint_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Movie API"}


def test_endpoint_get_movies(client):
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_endpoint_get_movie(client):
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
