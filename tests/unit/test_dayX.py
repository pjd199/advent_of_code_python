"""Runs the unit tests for each day, using input from test_cases.json."""
from datetime import date
from importlib import import_module
from importlib.util import find_spec
from re import compile
from secrets import choice, randbelow
from string import printable
from subprocess import run

import pytest

from advent_of_code.utils.input_loader import load_file, load_puzzle_input_file
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.utils.solver_status import implementation_status
from tests.conftest import Expected, Part


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate the parametised tests.

    Args:
        metafunc (pytest.Metafunc): the meta function
    """
    implemented = [
        puzzle for puzzle, status in implementation_status().items() if status
    ]
    if "puzzle" in metafunc.fixturenames:
        metafunc.parametrize(
            "puzzle",
            implemented,
            ids=[f"{d.year:04}-{d.day:02}" for d in implemented],
        )

    if "part" in metafunc.fixturenames:
        metafunc.parametrize(
            "part", [Part.ONE, Part.TWO, Part.ALL], ids=["part_one", "part_two", "all"]
        )


def test_module_spec(puzzle: date, expected: Expected) -> None:
    """Test the module exists and has a class of the right type.

    Args:
        puzzle (date): date object with year and day for the puzzle
        expected (Expected): the expected results
    """
    # check the module exists
    module_name = f"advent_of_code.year{puzzle.year}.day{puzzle.day}"
    assert find_spec(module_name) is not None, f"{module_name} does not exist"

    # load the module and check the class is correct subclass
    mod = import_module(f"advent_of_code.year{puzzle.year}.day{puzzle.day}")
    assert issubclass(mod.Solver, SolverInterface)

    # check the metadata
    assert mod.Solver.TITLE == expected[puzzle.year][puzzle.day]["title"]
    assert mod.Solver.YEAR == expected[puzzle.year][puzzle.day]["year"]
    assert mod.Solver.DAY == expected[puzzle.year][puzzle.day]["day"]


def test_load_test_file(puzzle: date) -> None:
    """Tests that all the required input files are available.

    Args:
        puzzle (date): date object with year and day for the puzzle
    """
    # check the input file exists and is not empty
    filename = f"./puzzle_input/year{puzzle.year}/day{puzzle.day}.txt"
    puzzle_input = load_file(filename)
    assert puzzle_input is not None, f"Unable to load {filename}"
    assert len(puzzle_input) > 0, f"{filename} has no content"
    assert puzzle_input[-1] != "", (
        f"trailing blank lines should have been removed " f"from {filename} "
    )


def test_init_solver(puzzle: date) -> None:
    """Test the solution accepts the puzzle input without raising an error.

    Args:
        puzzle (date): date object with year and day for the puzzle
    """
    # instantiate the class, which should not raise any expections
    mod = import_module(f"advent_of_code.year{puzzle.year}.day{puzzle.day}")
    mod.Solver(load_puzzle_input_file(puzzle.year, puzzle.day))

    # test with None input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver(None)

    # test with empty input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver([])

    # test with single "" input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver([""])

    # test with a single line of random input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver(["".join([choice(printable) for _ in range(randbelow(99) + 101)])])

    # test with multiple lines of random input, which should cause a problem
    with pytest.raises(RuntimeError):
        mod.Solver(
            [
                "".join([choice(printable) for _ in range(randbelow(99) + 101)])
                for _ in range(randbelow(99) + 101)
            ]
        )


def test_solve(puzzle: date, expected: Expected, part: Part) -> None:
    """Test the solution have the correct answers.

    Args:
        puzzle (date): date object with year and day for the puzzle
        expected (Expected) : the test cases
        part (Part): the part to run
    """
    # dynamically instantiate the class
    mod = import_module(f"advent_of_code.year{puzzle.year}.day{puzzle.day}")
    solver = mod.Solver(load_puzzle_input_file(puzzle.year, puzzle.day))

    if not (puzzle.day == 25 and part == Part.TWO):
        part_mapper = {
            Part.ALL: solver.solve_all,
            Part.ONE: lambda: [solver.solve_part_one(), None],
            Part.TWO: lambda: [None, solver.solve_part_two()],
        }
        answers = part_mapper[part]()
        if part in [Part.ONE, Part.ALL]:
            assert str(answers[0]) == expected[puzzle.year][puzzle.day]["part_one"]
        if part in [Part.TWO, Part.ALL] and puzzle.day != 25:
            assert str(answers[1]) == expected[puzzle.year][puzzle.day]["part_two"]
    else:
        with pytest.raises(NotImplementedError) as exception_info:
            answers = solver.solve_part_two()
        assert "NotImplementedError" in str(exception_info), (
            f"Found an answer for {puzzle.year} {puzzle.day}: "
            "expected to raise NotImplementedError"
        )


def test_cli(puzzle: date, expected: Expected) -> None:
    """Test the solution have the correct answers.

    Args:
        puzzle (date): date object with year and day for the puzzle
        expected (Expected): the expected results
    """
    # simulate command line execution, expecting no errors
    result = run(
        ["python", f"./advent_of_code/year{puzzle.year}/day{puzzle.day}.py"],
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
    assert m["title"] == expected[puzzle.year][puzzle.day]["title"]
    assert int(m["year"]) == expected[puzzle.year][puzzle.day]["year"]
    assert int(m["day"]) == expected[puzzle.year][puzzle.day]["day"]

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
            assert m["result"] == expected[puzzle.year][puzzle.day][f"part_{part}"]
            part = "two"

    assert part == "two" if (puzzle.day < 25) else "one"
