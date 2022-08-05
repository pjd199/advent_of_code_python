"""Unit test for advent_of_code.utils.runner."""
from json import load
from re import match

import pytest

from advent_of_code.utils.runner import runner
from advent_of_code.year2015.day1 import Solver


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
    assert lines[1] == "Solving part one: (0.00s)"
    assert match(
        rf"Solved part one: {test_cases['2015']['1'][0]} in \d+.\d\ds", lines[2]
    )
    assert lines[3] == "Solving part two: (0.00s)"
    assert match(
        rf"Solved part two: {test_cases['2015']['1'][1]} in \d+.\d\ds", lines[4]
    )
