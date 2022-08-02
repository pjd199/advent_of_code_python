"""Unit test for advent_of_code.utils.runner."""
from json import load
from re import match

import pytest

from advent_of_code.utils.runner import _format_time, runner
from advent_of_code.year2015.day1 import Solver


def test_format_time() -> None:
    """Unit test for _format_time()."""
    assert _format_time(1230000000) == "1.23s"


def test_runner(capfd: pytest.CaptureFixture[str]) -> None:
    """Unit test for runner().

    Args:
        capfd (pytest.CaptureFixture[str]): fixture to capture stdout
    """
    with open("./tests/unit/test_dayX.json") as file:
        test_cases = load(file)

    # execute runner and check for the expected output
    runner(Solver)
    captured = capfd.readouterr()
    lines = [x for x in captured.out.splitlines() if x]
    assert lines[0] == "Solving 'Not Quite Lisp' [2015-01]"
    assert match(
        rf"Solved part one: {test_cases['2015']['1'][0]} in \d+.\d\ds", lines[1]
    )
    assert match(
        rf"Solved part two: {test_cases['2015']['1'][1]} in \d+.\d\ds", lines[2]
    )
