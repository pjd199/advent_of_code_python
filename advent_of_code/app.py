"""Flask Application for Advent of Code Solver RESTful API."""
from datetime import datetime, timezone
from functools import cache
from importlib import import_module
from importlib.resources import files
from json import dumps, loads
from pathlib import Path
from platform import (
    architecture,
    machine,
    platform,
    python_implementation,
    python_version,
)
from sys import path
from typing import Any

from apig_wsgi import make_lambda_handler
from flask import Flask, Response, make_response, request
from requests import RequestException, get
from werkzeug.exceptions import HTTPException

if __name__ == "__main__":
    path.append(str(Path(__file__).parent.parent))  # pragma: no cover

from advent_of_code import __version__
from advent_of_code.utils.function_timer import function_timer
from advent_of_code.utils.input_loader import load_multi_line_string
from advent_of_code.utils.parser import ParseError
from advent_of_code.utils.solver_status import (
    implementation_status,
    is_solver_implemented,
)

# initialise the flask app
app = Flask(__name__)
lambda_handler = make_lambda_handler(app)

Json = int | float | str | bool | dict[str, Any] | list[Any] | None

Metadata = dict[str, dict[str, dict[str, int | str | bool | dict[str, int | str]]]]


@cache
def load_metadata_from_file() -> Metadata:
    """Load JSON metadata from a file, caching the result.

    Returns:
        Metadata: the JSON
    """
    result: Metadata = loads(
        files("advent_of_code").joinpath("puzzle_metadata.json").read_text()
    )
    return result


def standard_response(
    description: str,
    status: int = 200,
    results: Json = None,
    links: Json = None,
) -> Response:
    """Generate the standard body.

    Args:
        description (str): the descriptionn for this function
        status (int) : the HTTP status code, defaults to 200 (OK)
        results (Json): the results of the api call
        links (Json): the links associated with this api call

    Returns:
        Response: a response object
    """
    return make_response(
        dumps(
            {
                "timestamp": datetime.now(tz=timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "self": request.base_url.strip("/"),
                "api_version": __version__,
                "description": description,
                "results": results if results else [],
                "links": links if links else [],
            },
            sort_keys=False,
            indent=4,
        ),
        status,
        {
            "Cache-Control": "public, max-age=3600" if status == 200 else "no-cache",
            "Strict-Transport-Security": "max-age=3600; includeSubDomains; preload",
            "Content-Type": "application/json",
        },
    )


@app.route("/", methods=["GET"])
def handle_root_path() -> Response:
    """Handle the root path - / .

    Returns:
        Response: the response object
    """
    results = ["calendars", "puzzles", "answers"]
    links = [
        {
            "rel": "calendars",
            "href": f"{request.host_url.strip('/')}/calendars",
            "description": "Discover available puzzles and answers, "
            "filtered using /calendars/{year}.",
            "action": "GET",
        },
        {
            "rel": "puzzles",
            "href": f"{request.host_url.strip('/')}/puzzles",
            "description": "Discover detailed puzzle information, "
            "filtered using /puzzles/{year}/{day}.",
            "action": "GET",
        },
        {
            "rel": "answers",
            "href": f"{request.host_url.strip('/')}/answers",
            "description": "Find answer for given input by calling "
            "/answers/{year}/{day} with puzzle input as POST body "
            "or URL provided as input paramerater.",
            "action": "GET",
            "parameters": ["input"],
        },
        {
            "rel": "answers",
            "href": f"{request.host_url.strip('/')}/answers",
            "description": "Find answer for given input by calling "
            "/answers/{year}/{day} with puzzle input as POST body "
            "or URL provided as input paramerater.",
            "action": "POST",
        },
    ]

    return standard_response(
        "Discover resourses available through this API.", 200, results, links
    )


@app.route("/calendars", methods=["GET"])
@app.route("/calendars/", methods=["GET"])
@app.route("/calendars/<int:year_filter>", methods=["GET"])
@app.route("/calendars/<int:year_filter>/", methods=["GET"])
def handle_calendars_path(
    year_filter: int | None = None,
) -> Response:
    """Handle the root path - /calendars .

    Args:
        year_filter (int | None): The year_filter element from the URL

    Returns:
        Response: the response object
    """
    results = [
        {
            "year": year,
            "days": [
                x.day
                for x, status in implementation_status().items()
                if status and x.year == year
            ],
            "links": [
                {
                    "rel": "puzzles",
                    "href": f"{request.host_url.strip('/')}/puzzles/{year}",
                    "description": f"Discover detailed puzzle information "
                    f"for {year}.",
                    "action": "GET",
                },
            ],
        }
        for year in sorted({date.year for date in implementation_status()})
        if year_filter is None or year_filter == year
    ]

    return standard_response(
        "List of available puzzles, filtered using /calendars/{year}",
        200,
        results,
    )


@app.route("/puzzles", methods=["GET"])
@app.route("/puzzles/", methods=["GET"])
@app.route("/puzzles/<int:year_filter>", methods=["GET"])
@app.route("/puzzles/<int:year_filter>/", methods=["GET"])
@app.route("/puzzles/<int:year_filter>/<int:day_filter>", methods=["GET"])
@app.route("/puzzles/<int:year_filter>/<int:day_filter>/", methods=["GET"])
def handle_puzzles_path(
    year_filter: (int | None) = None, day_filter: (int | None) = None
) -> Response:
    """Handle the root path - /puzzles .

    Args:
        year_filter (int | None): The year_filter element from the URL
        day_filter (int | None): The day_filter element from the URL

    Returns:
        Response: the response object
    """
    metadata = load_metadata_from_file()

    results = [
        {
            "year": year,
            "day": day,
            "title": metadata[str(year)][str(day)]["title"],
            "excerpt": metadata[str(year)][str(day)]["excerpt"],
            "has_part_one": metadata[str(year)][str(day)]["has_part_one"],
            "has_part_two": metadata[str(year)][str(day)]["has_part_two"],
            "part_one_solved": metadata[str(year)][str(day)]["part_one_solved"],
            "part_two_solved": metadata[str(year)][str(day)]["part_two_solved"],
            "completion_date": metadata[str(year)][str(day)]["completion_date"],
            "timings": metadata[str(year)][str(day)]["timings"],
            "official_url": f"https://adventofcode.com/{year}/day/{day}",
            "repository_url": "https://github.com/pjd199/advent_of_code_python"
            f"/blob/main/advent_of_code/year{year}/day{day}.py",
            "code_url": "https://raw.githubusercontent.com/pjd199/advent_of_code_python"
            f"/main/advent_of_code/year{year}/day{day}.py",
            "links": [
                {
                    "rel": "answers",
                    "href": f"{request.host_url.strip('/')}/answers/{year}/{day}",
                    "description": f"Get the answer for {year} day {day}.",
                    "action": "GET",
                    "parameters": ["input"],
                },
                {
                    "rel": "answers",
                    "href": f"{request.host_url.strip('/')}/answers/{year}/{day}",
                    "description": f"Get the answer for {year} day {day}.",
                    "action": "POST",
                },
            ],
        }
        for year, day in sorted(
            {
                (date.year, date.day)
                for date, status in implementation_status().items()
                if status
            }
        )
        if (year_filter is None or year_filter == year)
        and (day_filter is None or day_filter == day)
    ]

    return standard_response(
        "Detailed puzzle information, filtered using /puzzles/{year}/{day}",
        200,
        results,
    )


@app.route("/answers/<int:year>/<int:day>", methods=["GET", "POST"])
@app.route("/answers/<int:year>/<int:day>/", methods=["GET", "POST"])
def handle_answers_path(year: int, day: int) -> Response:
    """Handle the solve all parts path - eg /2015/1.

    Args:
        year (int): the year from the path
        day (int): the  day from the path

    Returns:
        Response: the standard response object
    """

    def error_response(text: str) -> Response:
        return standard_response(
            "Get the answer to the puzzle, with input file provide as POST, "
            "or URL provided as input paramerater.",
            400,
            text,
        )

    if not is_solver_implemented(year, day):
        return error_response(
            f"year {year} day {day} is invalid. "
            f"Please call {request.host_url.strip('/')}/calendars for valid values.",
        )

    # load the input data
    text = ""
    if (
        request.method == "POST"
        and request.content_type == "text/plain"
        and request.content_length
        and 0 < request.content_length < 1048576
    ):
        text = request.get_data(as_text=True)
    elif "input" in request.args:
        try:
            text = get(request.args["input"], timeout=60).text
        except RequestException:
            return error_response(
                f"Unable to GET puzzle input from {request.args['input']}.",
            )
    else:
        return error_response(
            "Unable to load the input data. Send fine as a text/plain POST, "
            "or URL provided with the URL input paramerater.",
        )

    puzzle_input = load_multi_line_string(text)
    results: dict[str, Any] = {"year": year, "day": day}
    timing: dict[str, str | int] = {"units": "ms"}

    # load the solver and parse
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    try:
        solver, timing["parse"] = function_timer(mod.Solver, puzzle_input)
    except ParseError as e:
        return error_response(f"{e}")

    # run the sovler to find the answers
    results["part_one"], timing["part_one"] = function_timer(
        lambda: str(solver.solve_part_one())
    )

    if day != 25:
        results["part_two"], timing["part_two"] = function_timer(
            lambda: str(solver.solve_part_two())
        )

    results["timings"] = timing

    links = [
        {
            "rel": "puzzles",
            "href": f"{request.host_url.strip('/')}/puzzles/{year}/{day}",
            "description": f"Get the puzzle information for {year} day {day}.",
            "action": "GET",
        }
    ]

    return standard_response(
        "Get the answer to the puzzle, with input file provide as POST, "
        "or URL provided as input paramerater.",
        200,
        results,
        links,
    )


@app.route("/system", methods=["GET"])
@app.route("/system/", methods=["GET"])
def handle_system_path() -> Response:  # pragma: no cover
    """Handle the system path - /system/ .

    Returns:
        Response: return system information
    """
    results = {
        "url": request.url,
        "host": request.host,
        "platform": platform(),
        "machine": machine(),
        "architecture": architecture()[0],
        "compiler": f"{python_implementation()} {python_version()}",
        "license_url": "https://raw.githubusercontent.com/pjd199/advent_of_code_python"
        "/main/license.md",
        "license": "MIT",
        "event": request.environ["apig_wsgi.full_event"]
        if "apig_wsgi.full_event" in request.environ
        else {},
    }

    return standard_response("System information.", 200, results)


@app.errorhandler(HTTPException)
def handle_exception(e: HTTPException) -> Response:
    """Return JSON instead of HTML for HTTP errors.

    Args:
        e (HTTPException): the expection

    Returns:
        Response: the response
    """
    return standard_response(
        f"{e.description}",
        e.code if e.code is not None else 500,
        f"{e.name}",
    )
