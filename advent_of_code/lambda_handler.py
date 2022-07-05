"""Handler for AWS Lambda requests."""
from importlib import import_module
from json import dumps
from typing import Dict

from advent_of_code.utils.input_loader import load_file
from advent_of_code.utils.solver_status import (
    is_solver_implemented,
    solvers_implementation_status,
)


def lambda_handler(event: Dict[str, object], context: object) -> Dict[str, object]:
    """Handle the event from the AWS Lambda.

    Args:
        event (_type_): the event dictionary
        context (_type_): the context object

    Returns:
        _type_: the response sent to the client
    """
    path_param = [x for x in str(event["rawPath"]).lower().split("/") if x != ""]

    # /                      - list of available years
    # /year                  - list of available days for the year
    # /year/day              - solve both parts of the day
    # /year/day/part_one     - solve part one of the day
    # /year/day/part_two     - solve part two of the day

    # process / - list of available years
    body: Dict[str, object] = {}
    if len(path_param) == 0:
        dates = [
            date for date, status in solvers_implementation_status().items() if status
        ]
        body = {"years": list({x.year for x in dates})}
        status = 200

    # /year - list of available days for the year
    elif len(path_param) == 1 and path_param[0].isdecimal():
        year = int(path_param[0])
        dates = [
            date for date, status in solvers_implementation_status().items() if status
        ]
        body = {"days": list({x.day for x in dates if x.year == year})}
        status = 200

    # /year/day - solve both parts of the day
    elif (
        len(path_param) == 2
        and path_param[0].isdecimal()
        and path_param[1].isdecimal()
        and is_solver_implemented(int(path_param[0]), int(path_param[1]))
    ):
        year = int(path_param[0])
        day = int(path_param[1])
        puzzle_input = load_file(f"./tests/input/{year}/{day}.txt")
        mod = import_module(f"advent_of_code.year_{year}.day{day}")
        solver = mod.Solver(puzzle_input)
        results = solver.solve_all()

        if len(results) == 1:
            body = {
                "year": year,
                "day": day,
                "part_one": str(results[0]),
            }
        else:
            body = {
                "year": year,
                "day": day,
                "part_one": str(results[0]),
                "part_two": str(results[1]),
            }
        status = 200

    # /year/day/part_one - solve part one of the day
    # /year/day/part_two - solve part two of the day
    elif (
        len(path_param) == 3
        and path_param[0].isdecimal()
        and path_param[1].isdecimal()
        and path_param[2] in ["part_one", "part_two"]
        and is_solver_implemented(int(path_param[0]), int(path_param[1]))
        and (int(path_param[1]) != 25 or path_param[2] == "part_one")
    ):
        year = int(path_param[0])
        day = int(path_param[1])
        puzzle_input = load_file(f"./tests/input/{year}/{day}.txt")
        mod = import_module(f"advent_of_code.year_{year}.day{day}")
        solver = mod.Solver(puzzle_input)

        body = {"year": year, "day": day}
        if path_param[2] == "part_one":
            body |= {"part_one": str(solver.solve_part_one())}
        else:
            body |= {"part_two": str(solver.solve_part_two())}
        status = 200

    # unknown path
    else:
        body = {"message": f"Unknown path: /{'/'.join(path_param)}"}
        status = 404

    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": dumps(body),
    }
