"""Unit tests for the lambda_handler function."""
from json import load
from typing import Any, Dict, Iterable

import pytest
from flask.testing import FlaskClient
from freezegun import freeze_time
from werkzeug.test import TestResponse

from advent_of_code.app import app


@pytest.fixture(scope="module")
def test_client() -> Iterable[FlaskClient]:
    """Load the Flask test client.

    Yields:
        _type_: the test client
    """
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield test_client
    ctx.pop()


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    with open("./tests/integration/test_flask_app.json") as file:
        if "test_case" in metafunc.fixturenames:
            cases = load(file)["tests"]
            ids = [
                f"{data['request']['method']}{data['request']['path']}"
                for data in cases
            ]
            metafunc.parametrize("test_case", cases, ids=ids)


def test_routes(test_case: Dict["str", Any], test_client: FlaskClient) -> None:
    """Integration test for GET method.

    Args:
        test_case (Json): the test case data
        test_client: the Flask test client
    """

    def send_request() -> TestResponse:
        if test_case["request"]["method"] == "GET":
            return test_client.get(test_case["request"]["path"])
        elif "body" in test_case["request"] and "content_type" in test_case["request"]:
            return test_client.post(
                test_case["request"]["path"],
                data=test_case["request"]["body"],
                content_type=test_case["request"]["content_type"],
            )
        else:
            return test_client.post(test_case["request"]["path"])

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
