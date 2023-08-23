"""Unit tests for advent_of_code.utils.solver_status."""
from datetime import date

from advent_of_code.utils.solver_status import (
    first_puzzle_date,
    implementation_status,
    is_solver_implemented,
    last_puzzle_date,
    puzzle_date_generator,
)
from freezegun import freeze_time


def test_first_puzzle_date() -> None:
    """Unit test."""
    assert first_puzzle_date() == date(2015, 12, 1)


def test_last_puzzle_date() -> None:
    """Unit test."""
    # test for a date in December
    with freeze_time("2015-12-10"):
        assert last_puzzle_date() == date(2015, 12, 10)

    # test for a way in the future date in December
    with freeze_time("2100-12-1"):
        assert last_puzzle_date() == date(2100, 12, 1)

    # test for a boxing day
    with freeze_time("2100-12-26"):
        assert last_puzzle_date() == date(2100, 12, 25)

    # test for new years day
    with freeze_time("2101-1-1"):
        assert last_puzzle_date() == date(2100, 12, 25)


def test_puzzle_date_generator() -> None:
    """Unit test."""
    # test with just one puzzle
    with freeze_time("2015-12-1"):
        assert list(puzzle_date_generator()) == [date(2015, 12, 1)]

    # test for date in the advent season
    with freeze_time("2015-12-25"):
        assert list(puzzle_date_generator()) == [
            date(2015, 12, x + 1) for x in range(25)
        ]

    # test for day after puzzle season
    with freeze_time("2015-12-26"):
        assert list(puzzle_date_generator()) == [
            date(2015, 12, x + 1) for x in range(25)
        ]

    # test for multiple years
    with freeze_time("2016-12-5"):
        assert list(puzzle_date_generator()) == [
            date(2015, 12, x + 1) for x in range(25)
        ] + [date(2016, 12, x + 1) for x in range(5)]


def test_is_solver_implemented() -> None:
    """Unit test."""
    assert is_solver_implemented(2015, 1)
    assert not is_solver_implemented(2100, 1)


def test_implementation_status() -> None:
    """Unit test."""
    # test with one puzzle
    with freeze_time("2015-12-1"):
        assert implementation_status() == {date(2015, 12, 1): True}

    # test with a full season of puzzles
    with freeze_time("2015-12-25"):
        assert implementation_status() == {
            date(2015, 12, day): True for day in range(1, 25 + 1)
        }

    # test the day after the puzzle season ends
    with freeze_time("2015-12-26"):
        assert implementation_status() == {
            date(2015, 12, day): True for day in range(1, 25 + 1)
        }

    # test for multiple years
    with freeze_time("2025-12-10"):
        assert implementation_status() == (
            {
                date(year, 12, day): is_solver_implemented(year, day)
                for year in range(2015, 2025 + 1)
                for day in range(1, 25 + 1)
                if date(year, 12, day) <= date(2025, 12, 10)
            }
        )
