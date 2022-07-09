"""Handler for AWS Lambda requests."""
from importlib import import_module
from typing import Any, Dict, Optional, Tuple

from flask import abort, request
from flask_aws_lambda import FlaskAwsLambda  # type: ignore
from requests import get
from werkzeug.exceptions import HTTPException

from advent_of_code.utils.input_loader import load_file, load_multi_line_string
from advent_of_code.utils.solver_status import (
    implementation_status,
    is_solver_implemented,
)

# constants for URL parameter positions
YEAR = 0
DAY = 1
PART = 2

# initialise the flask app
app = FlaskAwsLambda(__name__)


@app.route("/", methods=["GET"])
def handle_root_path() -> Tuple[Dict[str, Any], int]:
    """Handles the root path - / .

    Returns:
        tuple[Json, int]: a JSON response and a HTTP status number
    """
    dates = [date for date, status in implementation_status().items() if status]
    return {
        "years": [
            {"year": year, "days": [x.day for x in dates if x.year == year]}
            for year in {x.year for x in dates}
        ]
    }, 200


@app.route("/<int:year>", methods=["GET"])
def handle_year_path(year: int) -> Tuple[Dict[str, Any], int]:
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

    return {"year": year, "days": days}, 200


@app.route("/<int:year>/<int:day>", methods=["GET", "POST"])
@app.route("/<int:year>/<int:day>/<string:part>", methods=["GET", "POST"])
def handle_solve_path_with_part(
    year: int, day: int, part: Optional[str] = None
) -> Tuple[Dict[str, Any], int]:
    """Handles the solve all parts path - eg /2015/1 .

    Args:
        year (int): the year from the path
        day (int): the  day from the path
        part (Optional[str]): the part from the path

    Returns:
        tuple[Json, int]: a JSON response
    """
    if (
        not is_solver_implemented(year, day)
        or part not in [None, "part_one", "part_two"]
        or (request.method == "POST" and request.args.get("input"))
        or (day == 25 and part == "part_two")
    ):
        abort(404)

    # load the input data
    query_input = request.args.get("input")
    if request.method == "POST":
        puzzle_input = load_multi_line_string(request.get_data(as_text=True))
    elif query_input is not None:
        puzzle_input = load_multi_line_string(get(query_input).text)
    else:
        puzzle_input = load_file(f"./tests/input/{year}/{day}.txt")

    # find the solver
    mod = import_module(f"advent_of_code.year_{year}.day{day}")
    solver = mod.Solver(puzzle_input)

    # construct the body
    body = {}
    if part == "part_one":
        body["part_one"] = str(solver.solve_part_one())
    elif part == "part_two":
        body["part_two"] = str(solver.solve_part_two())
    else:
        results = solver.solve_all()
        body["part_one"] = str(results[0])
        if len(results) == 2:
            body["part_two"] = str(results[1])

    body["year"] = year
    body["day"] = day

    return body, 200


@app.errorhandler(HTTPException)
def handle_exception(e: HTTPException) -> Tuple[Dict[str, Any], int]:
    """Return JSON instead of HTML for HTTP errors.

    Args:
        e (HTTPException): the expection

    Returns:
        Dict[str, Any]: the response
    """
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }, e.code if e.code is not None else 500
