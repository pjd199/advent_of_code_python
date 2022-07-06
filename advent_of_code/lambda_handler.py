"""Handler for AWS Lambda requests."""
from importlib import import_module
from json import dumps
from typing import Any, Dict, List, Tuple

from requests import get

from advent_of_code.utils.input_loader import load_file, load_multi_line_string
from advent_of_code.utils.solver_status import (
    implementation_status,
    is_solver_implemented,
)

# constants for URL parameter positions
YEAR = 0
DAY = 1
PART = 2


def handle_root_path(path_param: List[str], event: Dict[str, Any]) -> Tuple[str, int]:
    """Handles the root path - / .

    Args:
        path_param (List[str]): the path, as a list of strings
        event (Dict[str, Any]): the HTTP event

    Returns:
        Tuple[str, int]: a JSON response
    """
    dates = [date for date, status in implementation_status().items() if status]
    body = {
        "years": [
            {"year": year, "days": [x.day for x in dates if x.year == year]}
            for year in {x.year for x in dates}
        ]
    }
    return (dumps(body), 200)


def handle_year_path(path_param: List[str], event: Dict[str, Any]) -> Tuple[str, int]:
    """Handles the year path - eg /2015 .

    Args:
        path_param (List[str]): the path, as a list of strings
        event (Dict[str, Any]): the HTTP event

    Returns:
        Tuple[str, int]: a JSON response
    """
    year = int(path_param[YEAR])
    dates = [date for date, status in implementation_status().items() if status]
    body = {"year": year, "days": [x.day for x in dates if x.year == year]}
    return (dumps(body), 200)


def handle_solve_path(path_param: List[str], event: Dict[str, Any]) -> Tuple[str, int]:
    """Handles the solver path - eg /2015/1, /2015/1/part_one, /2015/1/part_two .

    Args:
        path_param (List[str]): the path, as a list of strings
        event (Dict[str, Any]): the HTTP event

    Returns:
        Tuple[str, int]: a JSON response
    """
    # decode the year and day
    year = int(path_param[YEAR])
    day = int(path_param[DAY])

    # load the puzzle input from POST, query parameters, or default to test
    if event["requestContext"]["http"]["method"] == "POST" and "body" in event:
        puzzle_input = load_multi_line_string(event["body"])
    elif (
        event["requestContext"]["http"]["method"] == "GET"
        and "queryStringParameters" in event
        and "input" in event["queryStringParameters"]
    ):
        puzzle_input = load_multi_line_string(
            get(event["queryStringParameters"]["input"]).text
        )
    else:
        puzzle_input = load_file(f"./tests/input/{year}/{day}.txt")

    # find the solver
    mod = import_module(f"advent_of_code.year_{year}.day{day}")
    solver = mod.Solver(puzzle_input)

    # construct the body
    body: Dict[str, Any] = {"year": year, "day": day}

    if len(path_param) == 2:
        results = solver.solve_all()
        body |= {"part_one": str(results[0])}
        if len(results) == 2:
            body |= {"part_two": str(results[1])}
    elif path_param[2] == "part_one":
        body |= {"part_one": str(solver.solve_part_one())}
    else:
        body |= {"part_two": str(solver.solve_part_two())}

    return (dumps(body), 200)


def lambda_handler(event: Dict[str, Any], context: object) -> Dict[str, Any]:
    """Handle the event from the AWS Lambda.

    Args:
        event (Dict[str, object]): the event dictionary
        context (object): the context object

    Returns:
        _type_: the response sent to the client
    """
    path_param = [x for x in str(event["rawPath"]).lower().split("/") if x != ""]

    # /                      - list of available years
    # /year                  - list of available days for the year
    # /year/day              - solve both parts of the day
    # /year/day/part_one     - solve part one of the day
    # /year/day/part_two     - solve part two of the day

    body = ""
    status = 500

    try:
        # process / - list of available years
        if len(path_param) == 0:
            body, status = handle_root_path(path_param, event)

        # /year - list of available days for the year
        elif len(path_param) == 1 and path_param[YEAR].isdecimal():
            body, status = handle_year_path(path_param, event)

        # /year/day - solve both parts of the day
        # /year/day/part_one - solve part one of the day
        # /year/day/part_two - solve part two of the day
        elif (
            (2 <= len(path_param) <= 3)
            and path_param[YEAR].isdecimal()
            and path_param[DAY].isdecimal()
            and is_solver_implemented(int(path_param[YEAR]), int(path_param[DAY]))
            and (
                len(path_param) < 3
                or path_param[PART] == "part_one"
                or (path_param[PART] == "part_two" and int(path_param[DAY]) != 25)
            )
        ):
            body, status = handle_solve_path(path_param, event)

        # unknown path
        else:
            body = dumps({"message": f"Unknown path: {event['rawPath']}"})
            status = 404

    except Exception as e:
        body = dumps(
            {"message": f"Unable to process request for: {event['rawPath']} - {str(e)}"}
        )
        status = 500

    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": body,
    }
