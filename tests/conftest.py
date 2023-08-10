"""Fixtures shared accross the test suite."""
from enum import Enum, auto, unique
from json import load
from typing import Any, NewType

import pytest

Expected = NewType("Expected", dict[int, dict[int, dict[str, int | str]]])

Json = dict[str, Any] | list[Any] | str | int | float | bool | None


@unique
class Part(Enum):
    """Enumeration of parts."""

    ONE = auto()
    TWO = auto()


@pytest.fixture(scope="module")
def expected() -> Expected:
    """Load the test cases from the json file.

        JSON format only allows string keys, but we want int keys,
        for map the string number keys to int number keys.

    Returns:
        Expected: The test case data
    """
    with open("./tests/expected.json") as file:
        return Expected(
            {
                int(year): {int(day): value for day, value in inner.items()}
                for year, inner in load(file).items()
            }
        )


def check_json(
    left: Json,
    right: Json,
    skip: list[str] | None = None,
    replace: list[tuple[str, str]] | None = None,
    path: str = "$",
) -> None:
    """Check for equality between two JSON objects.

    Args:
        left (Json): the left JSON object
        right (Json): the right JSON object
        skip (list[str] | None): keys to skip during compare.
        replace(list[tuple[str, str]] | None): strings to replace during compare
        path (str): path to track recursion
    """
    if isinstance(left, dict) and isinstance(right, dict):
        # compare dictionaries, catering for skip keys
        for key in left.keys() | right.keys():
            if skip is None or key not in skip:
                assert key in left, f"{key} is not in left at {path}"
                assert key in right, f"{key} is not in right at {path}"
                check_json(left[key], right[key], skip, replace, f"{path}['{key}']")
    elif isinstance(left, list) and isinstance(right, list):
        # compare lists
        assert len(left) == len(
            right
        ), f"List length mismatch ({len(left)} != {len(right)}) at {path}"
        for i, (x, y) in enumerate(zip(left, right)):
            check_json(x, y, skip, replace, f"{path}['{i}']")
    elif replace is not None and isinstance(left, str) and isinstance(right, str):
        # compare strings, with replacement
        left1, right1 = left, right
        for old, new in replace:
            left1 = left1.replace(old, new)
            right1 = right1.replace(old, new)
        assert left1 == right1, f"{left} != {right} at {path}\n{left1} != {right1}"
    else:
        # compare other types
        assert left == right, f"{left} != {right} at {path}"
