"""Fixtures shared accross the test suite."""
from enum import Enum, auto, unique
from json import load
from typing import Dict, NewType, Union

import pytest

Expected = NewType("Expected", Dict[int, Dict[int, Dict[str, Union[int, str]]]])


@unique
class Part(Enum):
    """Enumeration of parts."""

    ALL = auto()
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
