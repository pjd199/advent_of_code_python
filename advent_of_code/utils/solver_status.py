"""Functions based on the implementation status of solvers."""
from datetime import date
from email.generator import Generator
from importlib.util import find_spec
from typing import Dict, Iterable


def first_puzzle_date() -> date:
    """Return the date of the first challenge on Aoc Website.

    Returns:
        date: the first challenge date - always returns 2015/12/1.
    """
    return date(2015, 12, 1)


def last_puzzle_date() -> date:
    """Return the date of the last challenge on AoC website.

    Returns:
        date: the latest challenge date
    """
    today = date.today()

    if today.month <= 12:
        return date(today.year - 1, 12, 25)
    else:
        return date(today.year, 12, min(today.day, 25))


def puzzle_date_generator() -> Iterable[date]:
    """Generate a list of all puzzles on the AoC website.

    Yields:
        Iterable: _description_
    """
    today = date.today()

    # generate for previous years
    for year in range(first_puzzle_date().year, today.year):
        for day in range(1, 26):
            yield date(year, 12, day)

    # generate current year, if in the advent season (1st - 25th Dec)
    if today.month == 12:
        for day in range(1, today.day + 1):
            yield date(today.year, 12, day)


def is_solver_implemented(year: int, day: int) -> bool:
    """Returns True if solver is implemented, otherwise False.

    Args:
        year (int): The year
        day (int): The day

    Returns:
        bool: Returns True if solver is implemented, otherwise False.
    """
    try:
        find_spec(f"advent_of_code.year_{year}.day{day}")
        return True
    except ModuleNotFoundError:
        return False


def solvers_implementation_status() -> Dict[date, bool]:
    """Create a dictionary mapping AoC dates to implementation status.

    Returns:
        Dict[date, bool]: the dictionary
    """
    return {x: is_solver_implemented(x.year, x.day) for x in puzzle_date_generator()}
