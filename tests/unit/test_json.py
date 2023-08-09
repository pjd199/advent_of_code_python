"""Unit tests for advent_of_code.utils.json."""
from typing import Callable

import pytest

from tests.conftest import Json


def test_check_json(check_json: Callable[[Json, Json, list[str]], None]) -> None:
    """Unit test."""
    left = {
        "str": "value",
        "int": 123,
        "float": 0.5,
        "bool": True,
        "nested": [{"p": "q"}, {"r": "s"}],
        "list": ["a", "b", "c"],
        "dict": {"x": "1", "y": 2, "z": 3.0},
    }
    right = {
        "str": "value",
        "int": 123,
        "float": 0.5,
        "bool": True,
        "list": ["a", "b", "c", "d"],
        "nested": [{"p": "q"}, {"r": "s"}],
        "dict": {"x": "1", "y": 2, "z": 3.0, "w": 4},
    }
    with pytest.raises(AssertionError):
        check_json(left, right, [])

    check_json(left, right, ["list", "w"])

    with pytest.raises(AssertionError):
        check_json(left, right, ["list"])

    with pytest.raises(AssertionError):
        check_json(left, right, ["w"])

    check_json(left, right, ["list", "dict"])
