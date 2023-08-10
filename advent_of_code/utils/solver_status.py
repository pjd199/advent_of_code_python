"""Functions based on the implementation status of solvers."""
from collections.abc import Generator
from datetime import date, datetime, timezone
from importlib import import_module


def first_puzzle_date() -> date:
    """Return the date of the first challenge on Aoc Website.

    Returns:
        date: the first challenge date - always returns 2015/12/1.
    """
    return date(2015, 12, 1)


def last_puzzle_date() -> date:
    """Return the date of the last challenge on AoC website.

    Raises:
        RuntimeError: if the clock is wrong

    Returns:
        date: the latest challenge date
    """
    today = datetime.now(timezone.utc).date()

    if today < first_puzzle_date():
        raise RuntimeError(f"Today's date cannot be before {first_puzzle_date()}")

    if today.month < 12 and today.year > 2015:
        return date(today.year - 1, 12, 25)
    else:
        return date(today.year, 12, min(today.day, 25))


def puzzle_date_generator() -> Generator[date, None, None]:
    """Generate a list of all puzzles on the AoC website.

    Raises:
        RuntimeError: if the clock is wrong

    Yields:
        Generator[date, None, None]: All the puzzle dates
    """
    today = datetime.now(timezone.utc).date()

    if today < first_puzzle_date():
        raise RuntimeError(f"Today's date cannot be before {first_puzzle_date()}")

    for year in range(first_puzzle_date().year, today.year + 1):
        for day in range(1, 25 + 1):
            if date(year, 12, day) <= today:
                yield date(year, 12, day)


def is_solver_implemented(year: int, day: int) -> bool:
    """Returns True if solver is implemented, otherwise False.

    Args:
        year (int): The year
        day (int): The day

    Returns:
        bool: Returns True if solver is implemented, otherwise False.
    """
    try:
        import_module(f"advent_of_code.year{year}.day{day}")
        return True
    except ModuleNotFoundError:
        return False


def implementation_status() -> dict[date, bool]:
    """Create a dictionary mapping AoC dates to implementation status.

    Returns:
        dict[date, bool]: the dictionary
    """
    return {x: is_solver_implemented(x.year, x.day) for x in puzzle_date_generator()}
