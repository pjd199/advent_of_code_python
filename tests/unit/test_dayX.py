"""Runs the unit tests for each day, using input from test_cases.json."""
from importlib import import_module
from importlib.util import find_spec
from json import load
from secrets import choice, randbelow
from string import printable

import pytest

from advent_of_code.utils.input_loader import load_file
from advent_of_code.utils.solver_interface import SolverInterface

with open("./tests/unit/test_dayX.json") as file:
    test_cases = load(file)


@pytest.mark.parametrize(
    ("year", "day"),
    [(year, day) for year, days in test_cases.items() for day in days],
    ids=[
        f"{int(year):04}-{int(day):02}"
        for year, days in test_cases.items()
        for day in days
    ],
)
def test_module_spec(year: str, day: str) -> None:
    """Test the module exists and has a class of the right type.

    Args:
        year (str): The year to test
        day (str): the day to test
    """
    # check the module exists
    module_name = f"advent_of_code.year{year}.day{day}"
    assert find_spec(module_name) is not None, f"{module_name} does not exist"

    # load the module and check the class is correct subclass
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    assert issubclass(mod.Solver, SolverInterface)


@pytest.mark.parametrize(
    ("year", "day"),
    [(year, day) for year, days in test_cases.items() for day in days],
    ids=[
        f"{int(year):04}-{int(day):02}"
        for year, days in test_cases.items()
        for day in days
    ],
)
def test_load_test_file(year: str, day: str) -> None:
    """Tests that all the required input files are available.

    Args:
        year (str): The year to test
        day (str): the day to test
    """
    # check the input file exists and is not empty
    filename = f"./puzzle_input/year{year}/{day}.txt"
    puzzle_input = load_file(filename)
    assert puzzle_input is not None, f"Unable to load {filename}"
    assert len(puzzle_input) > 0, f"{filename} has no content"
    assert puzzle_input[-1] != "", (
        f"trailing blank lines should have been removed " f"from {filename} "
    )


@pytest.mark.parametrize(
    ("year", "day"),
    [(year, day) for year, days in test_cases.items() for day in days],
    ids=[
        f"{int(year):04}-{int(day):02}"
        for year, days in test_cases.items()
        for day in days
    ],
)
def test_init_solver(year: str, day: str) -> None:
    """Test the solution accepts the puzzle input without raising an error.

    Args:
        year (str): The year to test
        day (str): the day to test
    """
    # load the input file
    puzzle_input = load_file(f"./puzzle_input/year{year}/{day}.txt")

    # instantiate the class, which should not raise any expections
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    mod.Solver(puzzle_input)

    # test with None input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver(None)

    # test with empty input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver([])

    # test with single "" input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver([""])

    # first test with random input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver(
            [
                "".join([choice(printable) for _ in range(randbelow(99) + 101)])
                for _ in range(randbelow(99) + 101)
            ]
        )


@pytest.mark.parametrize(
    ("year", "day"),
    [(year, day) for year, days in test_cases.items() for day in days],
    ids=[
        f"{int(year):04}-{int(day):02}"
        for year, days in test_cases.items()
        for day in days
    ],
)
def test_solve_part_one(year: str, day: str) -> None:
    """Test the solution has the correct answer for part one.

    Args:
        year (str): The year to test
        day (str): the day to test
    """
    # load the input file
    puzzle_input = load_file(f"./puzzle_input/year{year}/{day}.txt")

    # instantiate the class
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    solver = mod.Solver(puzzle_input)

    # check the result
    answer = str(solver.solve_part_one())
    expected = test_cases[year][day][0]
    assert expected == answer, (
        f"Incorrect part one answer for {year} {day}: "
        f"expected {expected}, found {answer}"
    )


@pytest.mark.parametrize(
    ("year", "day"),
    [(year, day) for year, days in test_cases.items() for day in days],
    ids=[
        f"{int(year):04}-{int(day):02}"
        for year, days in test_cases.items()
        for day in days
    ],
)
def test_solve_part_two(year: str, day: str) -> None:
    """Test the solution have the correct answers.

    Args:
        year (str): The year to test
        day (str): the day to test
    """
    # load the input file
    puzzle_input = load_file(f"./puzzle_input/year{year}/{day}.txt")

    # dynamically instantiate the class
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    solver = mod.Solver(puzzle_input)

    # check the result - note day 25 doesn't have a part_two
    if day != "25":
        answer = str(solver.solve_part_two())
        expected = test_cases[year][day][1]
        assert expected == answer, (
            f"Incorrect part two answer for {year} {day}: "
            f"expected {expected}, found {answer}"
        )
    else:
        with pytest.raises(NotImplementedError) as exception_info:
            answer = solver.solve_part_two()
        assert "NotImplementedError" in str(exception_info), (
            "Found an answer for {year} {day}: " "expected to raise NotImplementedError"
        )


@pytest.mark.parametrize(
    ("year", "day"),
    [(year, day) for year, days in test_cases.items() for day in days],
    ids=[
        f"{int(year):04}-{int(day):02}"
        for year, days in test_cases.items()
        for day in days
    ],
)
def test_solve_all(year: str, day: str) -> None:
    """Test the solution have the correct answers.

    Args:
        year (str): The year to test
        day (str): the day to test
    """
    # load the input file
    puzzle_input = load_file(f"./puzzle_input/year{year}/{day}.txt")

    # dynamically instantiate the class
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    solver = mod.Solver(puzzle_input)

    # check the results
    answers = solver.solve_all()
    assert len(answers) == len(test_cases[year][day])
    for i, answer in enumerate(answers):
        expected = test_cases[year][day][i]
        assert expected == str(answer), (
            f"Incorrect answer in solve_all {year} {day} {i}: "
            f"expected {expected}, found {answer}"
        )
