"""Unit tests for the lambda_handler function."""
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
from advent_of_code import __version__
from advent_of_code.app import app
from advent_of_code.utils.solver_status import implementation_status
from freezegun import freeze_time
from werkzeug.test import TestResponse


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

    if (
        "year" in metafunc.fixturenames
        and "day" in metafunc.fixturenames
        and "expected" in metafunc.fixturenames
    ):
        with Path("./tests/expected.json").open() as file:
            test_data = load(file)

        implemented = [
            puzzle for puzzle, status in implementation_status().items() if status
        ]

        metafunc.parametrize(
            ("year", "day", "expected"),
            [(d.year, d.day, test_data[str(d.year)][str(d.day)]) for d in implemented],
            ids=[f"{d.year:04}-{d.day:02}" for d in implemented],
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
        pytest.check_json(  # type: ignore[operator]
            response.get_json(),
            test_case["response"]["body"],
            ["timings", "version", "event"],
            [("{version}", __version__)],
        )
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


def test_all_solver_routes(year: int, day: int, expected: dict[str, int | str]) -> None:
    """Test all expected routes - implemented or not.

    Args:
        year (int): year for the puzzle
        day (int): day for the puzzle
        expected (dict[str,int|str]): the expected results

    """
    with app.test_client() as client:
        with Path(f"./puzzle_input/year{year}/day{day}.txt").open() as file:
            input_file = file.read()
        response = client.post(
            f"/answers/{year}/{day}",
            data=input_file,
            headers={"Content-Type": "text/plain"},
            follow_redirects=True,
        )

    assert response.status_code == 200
    body = response.get_json()
    assert body is not None
    assert "results" in body
    assert body["results"]["year"] == year
    assert body["results"]["day"] == day
    assert "part_one" in body["results"]
    assert body["results"]["part_one"] == expected["part_one"]
    if day != 25:
        assert "part_two" in body["results"]
        assert body["results"]["part_two"] == expected["part_two"]
