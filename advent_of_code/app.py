"""Flask Application for Advent of Code Solver RESTful API."""
from importlib import import_module
from os import environ
from pathlib import Path
from sys import path
from threading import Thread
from time import perf_counter_ns, sleep
from typing import Any, Dict, Optional, Tuple

from flask import abort, request
from flask_aws_lambda import FlaskAwsLambda  # type: ignore
from requests import get
from werkzeug.exceptions import HTTPException

if __name__ == "__main__":
    path.append(str(Path(__file__).parent.parent))  # pragma: no cover

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


@app.route("/", methods=["GET"])  # type: ignore
def handle_root_path() -> Tuple[Dict[str, Any], int]:
    """Handles the root path - / .

    Returns:
        tuple[Json, int]: a JSON response and a HTTP status number
    """
    dates = [date for date, status in implementation_status().items() if status]
    return {
        "years": [
            {"year": year, "days": [x.day for x in dates if x.year == year]}
            for year in sorted({x.year for x in dates})
        ]
    }, 200


@app.route("/<int:year>/", methods=["GET"])  # type: ignore
@app.route("/<int:year>", methods=["GET"])  # type: ignore
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


@app.route("/<int:year>/<int:day>/", methods=["GET", "POST"])  # type: ignore
@app.route("/<int:year>/<int:day>", methods=["GET", "POST"])  # type: ignore
@app.route(
    "/<int:year>/<int:day>/<string:part>/", methods=["GET", "POST"]
)  # type: ignore
@app.route(
    "/<int:year>/<int:day>/<string:part>", methods=["GET", "POST"]
)  # type: ignore
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
        data = request.get_data()
        if isinstance(data, bytes):
            data = data.decode()
        puzzle_input = load_multi_line_string(data)
    elif query_input is not None:
        puzzle_input = load_multi_line_string(get(query_input).text)
    else:
        puzzle_input = load_file(f"./puzzle_input/year{year}/day{day}.txt")

    # find the solver
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    solver = mod.Solver(puzzle_input)

    # solve puzzle
    if part == "part_one" or day == 25:
        part_one, part_two = solver.solve_part_one(), None
    elif part == "part_two":
        part_one, part_two = None, str(solver.solve_part_two())
    else:
        part_one, part_two = solver.solve_all()

    # construct the body
    body: Dict[str, Any] = {"year": year, "day": day}
    if part_one:
        body["part_one"] = str(part_one)
    if part_two:
        body["part_two"] = str(part_two)

    return body, 200


@app.errorhandler(HTTPException)  # type: ignore
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


def main() -> None:  # pragma: no cover
    """Called when run from the command line."""
    # start the development server on the localhost
    host = "127.0.0.1"
    port = 5000
    environ["FLASK_ENV"] = "development"
    print(f"Starting development server on {host} at {port}")
    flask_thread = Thread(
        target=lambda: app.run(host=host, port=port, use_reloader=False)
    )
    flask_thread.daemon = True
    flask_thread.start()

    # allow the server time to start
    sleep(1)

    # print basic instructions
    print("---")
    print("Type 'exit' to shutdown server and exit")
    print("---")
    print("Available routes:")
    print(" - /")
    print(" - /{year}")
    print(" - /{year}/{day}")
    print(" - /{year}/{day}?input={url_for_puzzle_input_file}")
    print(" - /{year}/{day}/part_one")
    print(" - /{year}/{day}/part_two")
    print("eg - /2015/25")
    print("---")

    # loop until Ctrl-C exits the loop
    while True:
        print()
        url = input("Enter route path: ")
        if url in ["exit", "quit", "exit()"]:
            break

        try:
            # time the call to the development server
            start_time = perf_counter_ns()
            response = get(f"http://{host}:{port}{url}")
            end_time = perf_counter_ns()
            elapsed_time = end_time - start_time
            # print the time, then the response body in JSON
            if elapsed_time <= 1000000:
                print("Time: <1ms")
            elif elapsed_time >= 1000000000:
                print(f"Time: {elapsed_time / 1000000000:.2f}s")
            else:
                print(f"Time: {(elapsed_time) // 1000000}ms")
            print(response.json())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # run if file executed from the command line
    main()  # pragma: no cover
