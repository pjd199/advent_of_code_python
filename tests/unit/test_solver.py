"""Runs the unit tests for each day, using input from test_cases.json."""
from importlib import import_module
from importlib.util import find_spec
from json import load
from pathlib import Path
from re import compile
from secrets import choice, randbelow
from string import printable
from subprocess import run
from sys import executable

import pytest
from advent_of_code.utils.input_loader import load_file, load_puzzle_input_file
from advent_of_code.utils.parser import LengthError, ParseError
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.utils.solver_status import implementation_status


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    if (
        "year" in metafunc.fixturenames
        and "day" in metafunc.fixturenames
        and "expected" in metafunc.fixturenames
    ):
        with Path("./tests/expected.json").open() as file:
            test_data = load(file)

        implemented = [
            puzzle for puzzle, status in implementation_status().items() if status
        ]

        metafunc.parametrize(
            ("year", "day", "expected"),
            [(d.year, d.day, test_data[str(d.year)][str(d.day)]) for d in implemented],
            ids=[f"{d.year:04}-{d.day:02}" for d in implemented],
        )

    if (
        "year" in metafunc.fixturenames
        and "day" in metafunc.fixturenames
        and "expected" not in metafunc.fixturenames
    ):
        implemented = [
            puzzle for puzzle, status in implementation_status().items() if status
        ]

        metafunc.parametrize(
            ("year", "day"),
            [(d.year, d.day) for d in implemented],
            ids=[f"{d.year:04}-{d.day:02}" for d in implemented],
        )

    if "part" in metafunc.fixturenames:
        metafunc.parametrize("part", [1, 2], ids=["part_one", "part_two"])


def test_module_spec(year: int, day: int, expected: dict[str, int | str]) -> None:
    """Test the module exists and has a class of the right type.

    Args:
        year (int): year for the puzzle
        day (int): day for the puzzle
        expected (dict[str, int | str]): the expected results
    """
    # check the module exists
    module_name = f"advent_of_code.year{year}.day{day}"
    assert find_spec(module_name) is not None, f"{module_name} does not exist"

    # load the module and check the class is correct subclass
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    assert issubclass(mod.Solver, SolverInterface)

    # check the metadata
    assert expected["title"] == mod.Solver.TITLE
    assert expected["year"] == mod.Solver.YEAR
    assert expected["day"] == mod.Solver.DAY


def test_load_test_file(year: int, day: int) -> None:
    """Tests that all the required input files are available.

    Args:
        year (int): year for the puzzle
        day (int): day for the puzzle
    """
    # check the input file exists and is not empty
    filename = f"./puzzle_input/year{year}/day{day}.txt"
    puzzle_input = load_file(filename)
    assert puzzle_input is not None, f"Unable to load {filename}"
    assert len(puzzle_input) > 0, f"{filename} has no content"
    assert (
        puzzle_input[-1] != ""
    ), f"trailing blank lines should have been removed from {filename} "


def test_init_solver(year: int, day: int) -> None:
    """Test the solution accepts the puzzle input without raising an error.

    Args:
        year (int): year for the puzzle
        day (int): day for the puzzle
    """
    # instantiate the class, which should not raise any expections
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    mod.Solver(load_puzzle_input_file(year, day))

    # test with None input, which should cause a problem
    with pytest.raises(LengthError):
        mod.Solver(None)

    # test with empty input, which should cause a problem
    with pytest.raises(LengthError):
        mod.Solver([])

    # # test with single "" input, which should cause a problem
    with pytest.raises(ParseError):
        mod.Solver([""])

    # test with a single line of random input, which should cause a problem
    with pytest.raises((ParseError, ValueError)):
        mod.Solver(["".join([choice(printable) for _ in range(randbelow(99) + 101)])])

    # test with multiple lines of random input, which should cause a problem
    with pytest.raises((ParseError, ValueError)):
        mod.Solver(
            [
                "".join([choice(printable) for _ in range(randbelow(99) + 101)])
                for _ in range(randbelow(99) + 101)
            ]
        )


def test_solve(year: int, day: int, expected: dict[str, int | str], part: int) -> None:
    """Test the solution have the correct answers.

    Args:
        year (int): year for the puzzle
        day (int): day for the puzzle
        expected (dict[str, int | str]) : the test cases
        part (int): the part to run
    """
    # dynamically instantiate the class
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    solver = mod.Solver(load_puzzle_input_file(year, day))

    if part == 1:
        assert str(solver.solve_part_one()) == expected["part_one"]

    if part == 2:
        if day != 25:
            assert str(solver.solve_part_two()) == expected["part_two"]
        else:
            with pytest.raises(NotImplementedError) as exception_info:
                solver.solve_part_two()
            assert "NotImplementedError" in str(exception_info), (
                f"Found an answer for {year} {day}: "
                "expected to raise NotImplementedError"
            )


def test_cli(year: int, day: int, expected: dict[str, int | str]) -> None:
    """Test the solution have the correct answers.

    Args:
        year (int): year for the puzzle
        day (int): day for the puzzle
        expected (dict[str, int | str]): the expected results
    """
    # simulate command line execution, expecting no errors
    result = run(
        [executable, f"./advent_of_code/year{year}/day{day}.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert len(result.stderr) == 0
    lines = [x for x in result.stdout.splitlines() if x]

    # define regex patterns
    title_pattern = compile(
        r"Solving '(?P<title>.*)' \[(?P<year>\d{4})-(?P<day>\d{1,2})\]"
    )
    timer_pattern = compile(r"Solving part (?P<part>one|two): \((?P<time>\d+.\d\d)s\)")
    result_pattern = compile(
        r"Solved part (?P<part>one|two): (?P<result>.+) in \d+.\d\ds"
    )

    # match the title line
    m = title_pattern.fullmatch(lines[0])
    assert m is not None
    assert m["title"] == expected["title"]
    assert int(m["year"]) == expected["year"]
    assert int(m["day"]) == expected["day"]

    # loop through all the times, checking lines as expected
    total_time = 0.0
    part = "one"
    for line in lines[1:]:
        if m := timer_pattern.fullmatch(line):
            assert m["part"] == part
            time = float(m["time"])
            assert (time == 0.0) or (time > total_time)
            total_time = time
        else:
            m = result_pattern.fullmatch(line)
            assert m is not None
            assert m["part"] == part
            assert m["result"] == expected[f"part_{part}"]
            part = "two"

    assert part == "two" if (day < 25) else "one"
