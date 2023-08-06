"""Unit tests for advent_of_code.utils.json."""
from advent_of_code.utils.json import equals


def test_equals() -> None:
    """Unit test."""
    first = {
        "str": "value",
        "int": 123,
        "float": 0.5,
        "bool": True,
        "nested": [{"p": "q"}, {"r": "s"}],
        "list": ["a", "b", "c"],
        "dict": {"x": "1", "y": 2, "z": 3.0},
    }
    second = {
        "str": "value",
        "int": 123,
        "float": 0.5,
        "bool": True,
        "list": ["a", "b", "c", "d"],
        "nested": [{"p": "q"}, {"r": "s"}],
        "dict": {"x": "1", "y": 2, "z": 3.0, "w": 4},
    }
    assert not equals(first, second, [])
    assert equals(first, second, ["list", "w"])
    assert equals(first, second, ["list", "dict"])
