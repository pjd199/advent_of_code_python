"""System Tests."""
from json import load as load_json
from os import environ
from threading import Thread
from typing import Any, Dict

import pytest
from boto3 import client
from requests import get, post
from toml import load as load_toml

from advent_of_code.app import app
from advent_of_code.utils.solver_status import implementation_status


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    with open("./tests/system/system_test.json") as file:
        if "test_case" in metafunc.fixturenames:
            cases = load_json(file)["tests"]
            ids = [
                f"{data['request']['method']}{data['request']['path']}"
                for data in cases
            ]
            metafunc.parametrize("test_case", cases, ids=ids)


@pytest.fixture(scope="module")
def development_server() -> str:
    """Starts the development server on the localhost.

    Returns:
        str: the http url of the server
    """
    # start the development server on the localhost
    host = "127.0.0.1"
    port = 5000
    environ["FLASK_ENV"] = "development"
    flask_thread = Thread(
        target=lambda: app.run(host=host, port=port, use_reloader=False)
    )
    flask_thread.daemon = True
    flask_thread.start()

    return f"http://{host}:{port}"


@pytest.fixture(scope="module")
def lambda_urls() -> Dict[str, str]:
    """Open the SAM config file, and use the stack name to find the Fucntion URL.

    Returns:
        Dict[str, str]: the discovered urls, one for each file
    """
    urls = {}
    for file in ["./samconfig.toml", "./samconfig_dev.toml"]:
        try:
            sam_config = load_toml(file)
            stack_name = sam_config["default"]["deploy"]["parameters"]["stack_name"]
            region_name = sam_config["default"]["deploy"]["parameters"]["region"]

            cf_client = client("cloudformation", region_name=region_name)
            stack_descriptions = cf_client.describe_stacks(StackName=stack_name)

            if stack_descriptions["ResponseMetadata"]["HTTPStatusCode"] == 200:
                for stack in stack_descriptions["Stacks"]:
                    if stack["StackName"] == stack_name:
                        for output in stack["Outputs"]:
                            if output["OutputKey"] == "AdventOfCodeFunctionURL":
                                urls[file] = output["OutputValue"].strip("/")
                                break
        except Exception:
            ...
    return urls


def test_main(lambda_urls: Dict[str, str], test_case: Dict["str", Any]) -> None:
    """Test using the main branch Lambda Function URL.

    Args:
        lambda_urls (Dict[str, str]): the urls for testing
        test_case (Dict["str", Any]): the test case
    """
    call_lambda_function(lambda_urls["./samconfig.toml"], test_case)


def test_dev(lambda_urls: Dict[str, str], test_case: Dict["str", Any]) -> None:
    """Test using the development branch Lambda Function URL.

    Args:
        lambda_urls (Dict[str, str]): the urls for testing
        test_case (Dict["str", Any]): the test case
    """
    call_lambda_function(lambda_urls["./samconfig_dev.toml"], test_case)


def test_local(development_server: str, test_case: Dict["str", Any]) -> None:
    """Test using the main branch Lambda Function URL.

    Args:
        development_server (str): the fixture providing the server url
        test_case (Dict["str", Any]): the test case
    """
    call_lambda_function(development_server, test_case)


def call_lambda_function(url: str, test_case_data: Dict["str", Any]) -> None:
    """System test.

    Args:
        url (str): the Funciton URL of the deployed AWS Lambda function
        test_case_data (data: Dict["str", Any]): the test case data
    """
    # make the request
    if test_case_data["request"]["method"] == "GET":
        response = get(url + test_case_data["request"]["path"])
    elif (
        "body" in test_case_data["request"]
        and "content_type" in test_case_data["request"]
    ):
        response = post(
            url + test_case_data["request"]["path"],
            data=test_case_data["request"]["body"].encode(),
            headers={"Content-Type": test_case_data["request"]["content_type"]},
        )
    else:
        response = post(url + test_case_data["request"]["path"])

    # check the response code
    assert response.status_code == test_case_data["response"]["status"]

    # check the body, with "/" being the special case
    if test_case_data["request"]["path"] == "/calendars":
        dates = [date for date, status in implementation_status().items() if status]
        results = [
            {
                "days": [x.day for x in dates if x.year == year],
                "links": [
                    {
                        "action": "GET",
                        "description": "Discover detailed puzzle information"
                        f" for {year}.",
                        "href": f"http://api.adventofcode.dibdin.me/puzzles/{year}",
                        "rel": "puzzles",
                    }
                ],
                "year": year,
            }
            for year in sorted({x.year for x in dates})
        ]

        body = {
            "api_version": "2.0.0",
            "description": "List of available puzzles, filtered using "
            "/calendars/{year}",
            "links": [],
            "results": results,
            "self": "http://api.adventofcode.dibdin.me/calendars",
        }
        a = {k: v for k, v in response.json().items() if k != "timestamp"}

        assert a == body

    elif "body" in test_case_data["response"]:
        # check body is identical, ignoring timestamp and timings
        a = {k: v for k, v in response.json().items() if k != "timestamp"}
        b = {
            k: v
            for k, v in test_case_data["response"]["body"].items()
            if k != "timestamp"
        }
        if test_case_data["request"]["path"].startswith("/answers"):
            del a["results"]["timing"]
            del b["results"]["timing"]
        assert a == b
