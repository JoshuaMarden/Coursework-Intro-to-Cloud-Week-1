# pylint: skip-file

import pytest
from unittest.mock import patch
from api import app


@pytest.fixture
def sample_movie():
    return
    [{
        "movie_id": 3226,
        "names": "The Big Lebowski",
        "release_date_id": 3058,
        "score": 78.0,
        "synopsis": "Jeffrey 'The Dude' Lebowski, a Los Angeles slacker who only wants to bowl and drink White Russians, is mistaken for another Jeffrey Lebowski, a wheelchair-bound millionaire, and finds himself dragged into a strange series of events involving nihilists, adult film producers, ferrets, errant toes, and large sums of money.",
        "original_title": "The Big Lebowski",
        "release_status": "Released",
        "original_language_id": 29,
        "budget": 15000000,
        "revenue": 46189568,
        "country_id": 2,
        "language_id": 29,
        "original_language": " English",
        "date_id": 3058,
        "release_date": "Thu, 09 Apr 1998 00:00:00 GMT",
        "country": "AU",
        "genres": "Comedy, Crime"
    }]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_get_movies():
    with patch('api.get_movies') as mock:
        yield mock
