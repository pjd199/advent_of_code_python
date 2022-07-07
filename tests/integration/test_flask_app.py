"""Unit tests for the lambda_handler function."""
from json import load, loads

import pytest

from advent_of_code.app import app

with open("./tests/integration/test_flask_app.json") as file:
    test_cases = load(file)


@pytest.mark.parametrize(
    ("path", "status", "body"),
    [
        (
            data["path"],
            data["status"],
            loads(data["body"]),
        )
        for data in test_cases["GET"]
    ],
    ids=[data["path"] for data in test_cases["GET"]],
)
def test_get_path(path: str, status: int, body: str) -> None:
    """Integration test for GET method.

    Args:
        path (str): The path to request
        status (int): the status to expect
        body (str): the response body to expect
    """
    response = app.test_client().get(path)
    assert response.status_code == status
    assert response.get_json() == body
