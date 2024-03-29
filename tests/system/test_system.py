"""System Tests."""
from json import load as load_json
from os import environ
from pathlib import Path
from threading import Thread
from typing import Any

import pytest
from advent_of_code import __version__
from advent_of_code.app import app
from advent_of_code.utils.solver_status import implementation_status
from boto3 import client
from requests import get, post


def sam_url_lookup(stack_name: str, region_name: str) -> str:
    """Open the SAM config file, and use the stack name to find the Fucntion URL.

    Args:
        stack_name (str): the name of the AWS stack
        region_name (str): the name of the AWS region

    Returns:
        str: the discovered url
    """
    base_url = ""

    cf_client = client("cloudformation", region_name=region_name)
    stack_descriptions = cf_client.describe_stacks(StackName=stack_name)

    if stack_descriptions["ResponseMetadata"]["HTTPStatusCode"] == 200:
        for stack in stack_descriptions["Stacks"]:
            if stack["StackName"] == stack_name:
                for output in stack["Outputs"]:
                    if output["OutputKey"] == "AdventOfCodeFunctionURL":
                        base_url = output["OutputValue"].strip("/")
                        break

    return base_url


@pytest.fixture(scope="module")
def localhost_url() -> str:
    """Starts the development server on the localhost.

    Returns:
        str: the https url of the server
    """
    scheme = "https"
    host = "127.0.0.1"
    port = 5000

    # start the development server on the localhost
    environ["FLASK_ENV"] = "development"
    flask_thread = Thread(
        target=app.run,
        kwargs={
            "host": host,
            "port": port,
            "use_reloader": False,
            "ssl_context": "adhoc" if scheme == "https" else None,
        },
        daemon=True,
    )
    flask_thread.start()

    return f"{scheme}://{host}:{port}"


@pytest.fixture(scope="module")
def sam_dev_url() -> str:
    """The SAM development branch URL.

    Returns:
        str: The SAM development URL.
    """
    return sam_url_lookup("advent-of-code-python-dev2", "eu-west-2")


@pytest.fixture(scope="module")
def sam_main_url() -> str:
    """The SAM main branch URL.

    Returns:
        str: The SAM development URL.
    """
    return sam_url_lookup("advent-of-code-python2", "eu-west-2")


@pytest.fixture(scope="module")
def cdn_url(sam_main_url: str) -> str:
    """The CDN URL.

    Args:
        sam_main_url (str): the main URL

    Returns:
        str: The CDN URL
    """
    url = ""

    cf_client = client("cloudfront")
    dists = cf_client.list_distributions()

    for d in dists["DistributionList"]["Items"]:
        for o in d["Origins"]["Items"]:
            if sam_main_url == f"https://{o['DomainName']}":
                for alias in d["Aliases"]["Items"]:
                    url = f"https://{alias}"
                    break

    return url


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    with Path("./tests/system/system_test.json").open() as file:
        if "test_case" in metafunc.fixturenames:
            cases = load_json(file)["tests"]
            ids = [
                f"{data['request']['method']}{data['request']['path']}"
                for data in cases
            ]
            metafunc.parametrize("test_case", cases, ids=ids)


def test_main(sam_main_url: str, test_case: dict["str", Any]) -> None:
    """Test using the main branch Lambda Function URL.

    Args:
        sam_main_url (str): the url for testing
        test_case (dict["str", Any]): the test case
    """
    call_lambda_function(sam_main_url, test_case)


def test_cdn(cdn_url: str, test_case: dict["str", Any]) -> None:
    """Test using the CDN URL.

    Args:
        cdn_url (str): the url for testing
        test_case (dict["str", Any]): the test case
    """
    call_lambda_function(cdn_url, test_case)


def test_dev(sam_dev_url: str, test_case: dict["str", Any]) -> None:
    """Test using the development branch Lambda Function URL.

    Args:
        sam_dev_url (str): the url for testing
        test_case (dict["str", Any]): the test case
    """
    call_lambda_function(sam_dev_url, test_case)


def test_local(localhost_url: str, test_case: dict["str", Any]) -> None:
    """Test using the localhost URL.

    Args:
        localhost_url (str): the localhost URL
        test_case (dict["str", Any]): the test case
    """
    call_lambda_function(localhost_url, test_case)


def call_lambda_function(base_url: str, test_case_data: dict[str, Any]) -> None:
    """System test.

    Args:
        base_url (str): the Funciton URL of the deployed AWS Lambda function
        test_case_data (dict[str, Any]): the test case data
    """
    verify = "127.0.0.1" not in base_url

    # make the request
    if test_case_data["request"]["method"] == "GET":
        response = get(
            base_url + test_case_data["request"]["path"], verify=verify, timeout=300
        )
    elif (
        "body" in test_case_data["request"]
        and "content_type" in test_case_data["request"]
    ):
        response = post(
            base_url + test_case_data["request"]["path"],
            data=test_case_data["request"]["body"].encode(),
            headers={"Content-Type": test_case_data["request"]["content_type"]},
            verify=verify,
            timeout=300,
        )
    else:
        response = post(
            base_url + test_case_data["request"]["path"], verify=verify, timeout=300
        )

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
                        "href": f"{base_url}/puzzles/{year}",
                        "rel": "puzzles",
                    }
                ],
                "year": year,
            }
            for year in sorted({x.year for x in dates})
        ]

        body = {
            "api_version": "{version}",
            "description": "List of available puzzles, filtered using "
            "/calendars/{year}",
            "links": [],
            "results": results,
            "self": f"{base_url}/calendars",
        }
        pytest.check_json(  # type: ignore[operator]
            response.json(),
            body,
            ["timestamp", "version"],
            [("{version}", __version__)],
        )

    elif "body" in test_case_data["response"]:
        # check body is identical, ignoring timestamp and timings
        pytest.check_json(  # type: ignore[operator]
            response.json(),
            test_case_data["response"]["body"],
            ["timings", "timestamp", "version", "event"],
            [("{base_url}", base_url), ("{version}", __version__)],
        )
