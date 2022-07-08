"""Handler for AWS Lambda requests."""
from importlib import import_module
from json import dumps
from typing import Any

from flask import abort, request
from flask_aws_lambda import FlaskAwsLambda  # type: ignore
from requests import get
from werkzeug.exceptions import HTTPException

from advent_of_code.utils.input_loader import load_file, load_multi_line_string
from advent_of_code.utils.solver_status import (
    implementation_status,
    is_solver_implemented,
)

Json = dict[str, Any]

# constants for URL parameter positions
YEAR = 0
DAY = 1
PART = 2

# initialise the flask app
app = FlaskAwsLambda(__name__)


@app.route("/", methods=["GET"])
def handle_root_path() -> tuple[Json, int]:
    """Handles the root path - / .

    Returns:
        tuple[Json, int]: a JSON response and a HTTP status number
    """
    dates = [date for date, status in implementation_status().items() if status]
    body = {
        "years": [
            {"year": year, "days": [x.day for x in dates if x.year == year]}
            for year in {x.year for x in dates}
        ]
    }
    return body, 200


@app.route("/<int:year>", methods=["GET"])
def handle_year_path(year: int) -> tuple[Json, int]:
    """Handles the year path - eg /2015 .

    Args:
        year (int): the year from the path

    Returns:
        tuple[Json, int]: a JSON response
    """
    dates = [date for date, status in implementation_status().items() if status]
    days = [x.day for x in dates if x.year == year]
    if not days:
        abort(404)

    body = {"year": year, "days": days}
    return body, 200


def load_input() -> list[str]:
    # load the puzzle input from POST, query parameters, or default to test
    query_input = request.args.get("input")
    if request.method == "POST":
         return load_multi_line_string(request.get_data(as_text=True))
    elif query_input is not None:
        return load_multi_line_string(get(query_input).text)
    else:
        return load_file(f"./tests/input/{year}/{day}.txt")


@app.route("/<int:year>/<int:day>", methods=["GET", "POST"])
def handle_solve_path(year: int, day: int) -> tuple[Json, int]:
    """Handles the solve all parts path - eg /2015/1 .

    Args:
        year (int): the year from the path
        day (int): the  day from the path

    Returns:
        tuple[Json, int]: a JSON response
    """
    if not is_solver_implemented(year, day) or (
        request.method == "POST" and request.args.get("input")
    ):
        abort(404)

    # find the solver
    mod = import_module(f"advent_of_code.year_{year}.day{day}")
    solver = mod.Solver(load_input())
    results = solver.solve_all()

    # construct the body
    body = {"year": year, "day": day, "part_one": str(results[0])}
    if len(results) == 2:
        body |= {"part_two": str(results[1])}

    return body, 200


@app.route("/<int:year>/<int:day>/<string:part>", methods=["GET", "POST"])
def handle_solve_path_with_part(year: int, day: int, part: str) -> tuple[Json, int]:
    """Handles the solve all parts path - eg /2015/1 .

    Args:
        year (int): the year from the path
        day (int): the  day from the path
        part (str): the part from the path

    Returns:
        tuple[Json, int]: a JSON response
    """
    if not is_solver_implemented(year, day) or part not in ["part_one", "part_two"]:
        abort(404)

    # find the solver
    mod = import_module(f"advent_of_code.year_{year}.day{day}")
    solver = mod.Solver(load_input())

    # construct the body
    body: Json = {"year": year, "day": day}

    if part == "part_one":
        body = {"year": year, "day": day, "part_one": str(solver.solve_part_one())}
    else:
        body = {"year": year, "day": day, "part_two": str(solver.solve_part_two())}

    return body, 200


@app.errorhandler(404)
def page_not_found(e) -> tuple[Json, int]:
    """Handles the page not found error.

    Args:
        e (_type_): _description_

    Returns:
        Tuple[dict, int]: the response
    """
    return {"message": "Invalid path"}, 404


@app.errorhandler(HTTPException)
def handle_exception(e) -> tuple[Json, int]:
    """Return JSON instead of HTML for HTTP errors.

    Args:
        e (_type_): _description_

    Returns:
        Tuple[dict, int]: the response
    """
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
