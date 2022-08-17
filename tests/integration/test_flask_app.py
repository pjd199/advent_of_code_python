"""Unit tests for the lambda_handler function."""
from datetime import date
from json import load
from typing import Any, Dict, Iterable

import pytest
from flask.testing import FlaskClient
from freezegun import freeze_time
from werkzeug.test import TestResponse

from advent_of_code.app import app
from advent_of_code.utils.solver_status import (
    implementation_status,
    is_solver_implemented,
)
from tests.conftest import Expected


@pytest.fixture(scope="module")
def client() -> Iterable[FlaskClient]:
    """Load the Flask test client.

    Yields:
        _type_: the test client
    """
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    if "test_case" in metafunc.fixturenames:
        with open("./tests/integration/test_flask_app.json") as file:
            cases = load(file)["tests"]
            ids = [
                f"{data['request']['method']}{data['request']['path']}"
                for data in cases
            ]
            metafunc.parametrize("test_case", cases, ids=ids)

    all_dates = implementation_status().keys()
    if "puzzle" in metafunc.fixturenames:
        metafunc.parametrize(
            "puzzle",
            all_dates,
            ids=[f"{d.year:04}-{d.day:02}" for d in all_dates],
        )

    if "part" in metafunc.fixturenames:
        metafunc.parametrize("part", ["all", "part_one", "part_two"])


def test_other_routes(test_case: Dict["str", Any], client: FlaskClient) -> None:
    """Integration test for GET method.

    Args:
        test_case (Json): the test case data
        client: the Flask test client
    """

    def send_request() -> TestResponse:
        if test_case["request"]["method"] == "GET":
            return client.get(test_case["request"]["path"])
        elif "body" in test_case["request"] and "content_type" in test_case["request"]:
            return client.post(
                test_case["request"]["path"],
                data=test_case["request"]["body"],
                content_type=test_case["request"]["content_type"],
            )
        else:
            return client.post(test_case["request"]["path"])

    # set the time, if needed
    if "date" in test_case["request"]:
        with freeze_time(test_case["request"]["date"]):
            response = send_request()
    else:
        response = send_request()

    # check the response code and body
    assert response.status_code == test_case["response"]["status"]
    if "body" in test_case["response"]:
        assert response.get_json() == test_case["response"]["body"]


def test_all_solver_routes(
    puzzle: date,
    part: str,
    expected: Expected,
    client: FlaskClient,
) -> None:
    """Test all expected routes - implemented or not.

    Args:
        puzzle (date): the year and day to test
        part (str): the part to test
        expected (Expected): the expected results file
        client (FlaskClient): the FlaskClient

    Raises:
        AssertionError: Raised if the server gives a bad response
    """
    if part == "all":
        response = client.get(f"/{puzzle.year}/{puzzle.day}")
    else:
        response = client.get(f"/{puzzle.year}/{puzzle.day}/{part}")

    if response.status_code == 200:
        assert puzzle.year in expected
        assert puzzle.day in expected[puzzle.year]
        body = response.get_json()
        if body is not None:
            assert body["title"] == expected[puzzle.year][puzzle.day]["title"]
            assert body["year"] == puzzle.year
            assert body["day"] == puzzle.day
            if part in ["all", "part_one"]:
                assert body["part_one"] == expected[puzzle.year][puzzle.day]["part_one"]
            if part in ["all", "part_two"] and puzzle.day != 25:
                assert body["part_two"] == expected[puzzle.year][puzzle.day]["part_two"]
    elif response.status_code == 404:
        assert not is_solver_implemented(puzzle.year, puzzle.day) or (
            part == "part_two" and puzzle.day == 25
        )
    else:
        raise AssertionError(f"Received status_code {response.status_code}")
