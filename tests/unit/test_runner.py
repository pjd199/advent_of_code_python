"""Unit test for advent_of_code.utils.runner."""
from json import load
from pathlib import Path
from re import match

import pytest
from advent_of_code.utils.runner import runner
from advent_of_code.year2015.day1 import Solver


def test_runner(capfd: pytest.CaptureFixture[str]) -> None:
    """Unit test for runner().

    Args:
        capfd (pytest.CaptureFixture[str]): fixture to capture stdout
    """
    # load the details for day under test
    with Path("./tests/expected.json").open() as file:
        expected = load(file)["2015"]["1"]

    # execute runner and check for the expected output
    runner(Solver)
    captured = capfd.readouterr()
    lines = [x for x in captured.out.splitlines() if x]

    # assert the correct title
    m = match(r"Solving '(?P<title>.*)' \[(?P<year>\d\d\d\d)-(?P<day>\d\d)\]", lines[0])
    assert m
    assert m["title"] == expected["title"]
    assert int(m["year"]) == expected["year"]
    assert int(m["day"]) == expected["day"]

    # assert the correct part one
    assert match(r"Solving part one: \(0.00s\)", lines[1])
    m = match(r"Solved part one: (?P<part_one>.*) in \d+.\d\ds", lines[2])
    assert m
    assert m["part_one"] == expected["part_one"]

    # assert the correct part two
    assert match(r"Solving part two: \(0.00s\)", lines[3])
    m = match(r"Solved part two: (?P<part_two>.*) in \d+.\d\ds", lines[4])
    assert m
    assert m["part_two"] == expected["part_two"]
