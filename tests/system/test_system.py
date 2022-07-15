"""System Tests."""
from json import load as load_json
from os import scandir
from typing import Any, Dict

import pytest
from boto3 import client
from requests import Response, get, post
from toml import load as load_toml


def discover_url_from_config(sam_config_file: str) -> str:
    """Open the SAM config file, and use the stack name to find the Fucntion URL.

    Args:
        sam_config_file (str): the file name

    Returns:
        str: the discover url
    """
    sam_config = load_toml("./" + sam_config_file)
    stack_name = sam_config["default"]["deploy"]["parameters"]["stack_name"]
    region_name = sam_config["default"]["deploy"]["parameters"]["region"]

    cf_client = client("cloudformation", region_name=region_name)
    stack_descriptions = cf_client.describe_stacks(StackName=stack_name)

    url = ""
    if stack_descriptions["ResponseMetadata"]["HTTPStatusCode"] == 200:
        for stack in stack_descriptions["Stacks"]:
            if stack["StackName"] == stack_name:
                for output in stack["Outputs"]:
                    if output["OutputKey"] == "AdventOfCodeFunctionURL":
                        url = output["OutputValue"].strip("/")
                        break
    return url


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    with open("./tests/integration/test_flask_app.json") as file:
        if "test_case" in metafunc.fixturenames:
            cases = load_json(file)["tests"]
            ids = [
                f"{data['request']['method']}{data['request']['path']}"
                for data in cases
            ]
            metafunc.parametrize("test_case", cases, ids=ids)
        if "url" in metafunc.fixturenames:
            # find sam_config files
            sam_config_files = []
            with scandir() as scandir_iterator:
                for entry in scandir_iterator:
                    if (
                        entry.name.startswith("samconfig")
                        and entry.name.endswith(".toml")
                        and entry.is_file()
                    ):
                        sam_config_files.append(entry.name)
            urls = [discover_url_from_config(x) for x in sam_config_files]
            ids = [x.strip("samconfig_").strip(".toml") for x in sam_config_files]
            ids = [x if x else "main" for x in ids]
            metafunc.parametrize("url", urls, ids=ids)


def test_main(test_case: Dict["str", Any]) -> None:
    """Test using the main branch Lambda Function URL.

    Args:
        test_case (Dict["str", Any]): the test case
    """
    call_lambda_function(discover_url_from_config("samconfig.toml"), test_case)


def test_dev(test_case: Dict["str", Any]) -> None:
    """Test using the development branch Lambda Function URL.

    Args:
        test_case (Dict["str", Any]): the test case
    """
    call_lambda_function(discover_url_from_config("samconfig_dev.toml"), test_case)


def call_lambda_function(url: str, test_case_data: Dict["str", Any]) -> None:
    """System test.

    Args:
        url (str): the Funciton URL of the deployed AWS Lambda function
        test_case_data (data: Dict["str", Any]): the test case data
    """

    def send_request() -> Response:
        if test_case_data["request"]["method"] == "GET":
            return get(url + test_case_data["request"]["path"])
        elif (
            "body" in test_case_data["request"]
            and "content_type" in test_case_data["request"]
        ):
            return post(
                url + test_case_data["request"]["path"],
                data=test_case_data["request"]["body"].encode(),
                headers={"Content-Type": test_case_data["request"]["content_type"]},
            )
        else:
            return post(url + test_case_data["request"]["path"])

    # make the request
    response = send_request()

    # check the response code and body
    assert response.status_code == test_case_data["response"]["status"]
    if "body" in test_case_data["response"]:
        assert response.json() == test_case_data["response"]["body"]
