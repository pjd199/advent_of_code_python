"""Unit tests for the lambda_handler function."""
from datetime import date
from json import load
from pathlib import Path
from platform import (
    architecture,
    machine,
    platform,
    python_implementation,
    python_version,
)
from typing import Any

import pytest
from advent_of_code.app import app
from advent_of_code.utils.solver_status import implementation_status
from freezegun import freeze_time
from werkzeug.test import TestResponse

from tests.conftest import Expected, check_json


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    if "test_case" in metafunc.fixturenames:
        with Path("./tests/integration/test_flask_app.json").open() as file:
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


def test_other_routes(test_case: dict[str, Any]) -> None:
    """Integration test for GET method.

    Args:
        test_case (dict[str, Any]): the test case data
    """
    host = "localhost:5000"
    base_url = f"http://{host}"

    def send_request() -> TestResponse:
        with app.test_client() as client:
            if test_case["request"]["method"] == "GET":
                return client.get(test_case["request"]["path"], base_url=base_url)
            if (
                "body" in test_case["request"]
                and "content_type" in test_case["request"]
            ):
                return client.post(
                    test_case["request"]["path"],
                    data=test_case["request"]["body"],
                    content_type=test_case["request"]["content_type"],
                    base_url=base_url,
                )
            return client.post(test_case["request"]["path"], base_url=base_url)

    # set the time, if needed
    if "timestamp" in test_case["request"]:
        with freeze_time(test_case["request"]["timestamp"]):
            response = send_request()
    else:
        response = send_request()

    # check the response code and body, ignoring the timing value
    assert response.status_code == test_case["response"]["status"]

    # dynamically create the expected results on the system path
    if test_case["request"]["path"] == "/system":
        test_case["response"]["body"]["results"] = {
            "url": f"{base_url}/system",
            "host": host,
            "platform": platform(),
            "machine": machine(),
            "architecture": architecture()[0],
            "compiler": f"{python_implementation()} {python_version()}",
            "license_url": "https://raw.githubusercontent.com/pjd199/"
            "advent_of_code_python/main/license.md",
            "license": "MIT",
        }

    if "body" in test_case["response"]:
        # check the body, ignoring the timing value
        check_json(response.get_json(), test_case["response"]["body"], ["timings"])
        # check timings structure, but not values as they are variable
        if "results" in test_case["response"]["body"]:
            if "part_one" in test_case["response"]["body"]["results"]:
                assert "timings" in test_case["response"]["body"]["results"]
                assert isinstance(
                    test_case["response"]["body"]["results"]["timings"]["parse"], int
                )
                assert isinstance(
                    test_case["response"]["body"]["results"]["timings"]["part_one"], int
                )
                assert (
                    test_case["response"]["body"]["results"]["timings"]["units"] == "ms"
                )
            if "part_two" in test_case["response"]["body"]["results"]:
                assert isinstance(
                    test_case["response"]["body"]["results"]["timings"]["part_two"], int
                )


def test_all_solver_routes(puzzle: date, expected: Expected) -> None:
    """Test all expected routes - implemented or not.

    Args:
        puzzle (date): the year and day to test
        expected (Expected): the expected results file
    """
    with app.test_client() as client:
        with Path(
            f"./puzzle_input/year{puzzle.year}/day{puzzle.day}.txt"
        ).open() as file:
            input_file = file.read()
        response = client.post(
            f"/answers/{puzzle.year}/{puzzle.day}",
            data=input_file,
            headers={"Content-Type": "text/plain"},
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert puzzle.year in expected
    assert puzzle.day in expected[puzzle.year]
    body = response.get_json()
    assert body is not None
    assert "results" in body
    assert body["results"]["year"] == puzzle.year
    assert body["results"]["day"] == puzzle.day
    assert "part_one" in body["results"]
    assert body["results"]["part_one"] == expected[puzzle.year][puzzle.day]["part_one"]
    if puzzle.day != 25:
        assert "part_two" in body["results"]
        assert (
            body["results"]["part_two"] == expected[puzzle.year][puzzle.day]["part_two"]
        )
