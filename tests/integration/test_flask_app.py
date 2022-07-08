"""Unit tests for the lambda_handler function."""
from json import load
from typing import Any
import pytest

from advent_of_code.app import app

Json = dict["str", Any]


@pytest.fixture(scope="module")
def test_client():
    """Load the Flask test client.

    Yields:
        _type_: the test client
    """
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield test_client
    ctx.pop()


def pytest_generate_tests(metafunc: pytest.Metafunc):
    with open("./tests/integration/test_flask_app.json") as file:
        if "test_case" in metafunc.fixturenames:
            cases = load(file)["tests"]
            ids = [
                f"{data['request']['method']}{data['request']['path']}"
                for data in cases
            ]
            metafunc.parametrize("test_case", cases, ids=ids)


@pytest.fixture
def test_case(data):
    return data


def test_routes(test_case: Json, test_client) -> None:
    """Integration test for GET method.

    Args:
        test_case (Json): the test case data
        test_client: the Flask test client
    """
    if test_case["request"]["method"] == "GET":
        response = test_client.get(test_case["request"]["path"])
    elif "body" in test_case["request"] and "content_type" in test_case["request"]:
        response = test_client.post(
            test_case["request"]["path"],
            data=test_case["request"]["body"],
            content_type=test_case["request"]["content_type"],
        )
    else:
        response = test_client.post(test_case["request"]["path"])
    assert response.status_code == test_case["response"]["status"]
    if "body" in test_case["response"]:
        assert response.get_json() == test_case["response"]["body"]
