"""Unit tests for advent_of_code.utils.solver_status."""
from datetime import date, datetime
from importlib.util import find_spec

from advent_of_code.utils.solver_status import (
    first_puzzle_date,
    is_solver_implemented,
    last_puzzle_date,
    puzzle_date_generator,
    solvers_implementation_status,
)


def test_first_puzzle_date():
    """Unit test."""
    assert first_puzzle_date() == date(2015, 12, 1)


def test_last_puzzle_date():
    """Unit test."""
    if datetime.today().month < 12:
        assert last_puzzle_date() == date(datetime.today().year - 1, 12, 25)
    else:
        assert last_puzzle_date() == datetime.today()


def test_puzzle_date_generator():
    """Unit test."""
    dates = []
    for year in range(2015, datetime.today().year):
        for day in range(1, 26):
            dates.append(date(year, 12, day))
    if datetime.today().month == 12:
        for _ in range(1, datetime.today().day + 1):
            dates.append(datetime.today())

    assert list(puzzle_date_generator()) == dates


def test_is_solver_implemented():
    """Unit test."""
    assert is_solver_implemented(2015, 1)
    assert not is_solver_implemented(2014, 25)


def test_solvers_implementation_status():
    """Unit test."""
    dates = []
    for year in range(2015, datetime.today().year):
        for day in range(1, 26):
            dates.append(date(year, 12, day))
    if datetime.today().month == 12:
        for _ in range(1, datetime.today().day + 1):
            dates.append(datetime.today())

    status = {}
    for x in dates:
        try:
            find_spec(f"advent_of_code.year_{x.year}.day{x.day}")
            status[x] = True
        except ModuleNotFoundError:
            status[x] = False

    assert solvers_implementation_status() == status
