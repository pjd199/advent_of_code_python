"""Unit tests for advent_of_code.utils.parser."""
from dataclasses import dataclass
from enum import Enum
from re import fullmatch

import pytest

from advent_of_code.utils.parser import (
    ParseException,
    _validate_input_and_header,
    dataclass_processor,
    enum_processor,
    int_processor,
    int_processor_group,
    int_tuple_processor,
    parse_grid,
    parse_lines,
    parse_single_line,
    parse_tokens,
    str_processor,
    str_processor_group,
    str_tuple_processor,
)


def test_int_processor() -> None:
    """Unit test for int_processor."""
    m = fullmatch(r".*", "1234")
    assert m is not None
    assert int_processor(m) == 1234

    m = fullmatch(r".*", "-5678")
    assert m is not None
    assert int_processor(m) == -5678

    m = fullmatch(r".*", "abc")
    assert m is not None
    with pytest.raises(
        ValueError, match=r"invalid literal for int\(\) with base 10: 'abc'"
    ):
        int_processor(m)


def test_int_processor_group() -> None:
    """Unit test for int_processor_group."""
    m = fullmatch(r"(\d)(\d+)(\d)", "1234")
    assert m is not None
    assert int_processor_group(0)(m) == 1234
    assert int_processor_group(1)(m) == 1
    assert int_processor_group(2)(m) == 23
    assert int_processor_group(3)(m) == 4
    with pytest.raises(IndexError, match=r"no such group"):
        int_processor_group(4)(m)
    with pytest.raises(IndexError, match=r"no such group"):
        int_processor_group("value")(m)

    m = fullmatch(r"(?P<value>-?\d+)", "-5678")
    assert m is not None
    assert int_processor_group("value")(m) == -5678

    m = fullmatch(r".*", "abc")
    assert m is not None
    with pytest.raises(
        ValueError, match=r"invalid literal for int\(\) with base 10: 'abc'"
    ):
        int_processor_group(0)(m)


def test_int_tuple_processor() -> None:
    """Unit test for int_tuple_processor."""
    m = fullmatch(r"(.*) (.*) (.*)", "1 -2 3")
    assert m is not None
    assert int_tuple_processor(m) == (1, -2, 3)

    m = fullmatch(r"(.*) (.*) (.*)", "1 -2 c")
    assert m is not None
    with pytest.raises(
        ValueError, match=r"invalid literal for int\(\) with base 10: 'c'"
    ):
        int_tuple_processor(m)


def test_str_processor() -> None:
    """Unit test for str_processor."""
    m = fullmatch(r".*", "hello world")
    assert m is not None
    assert str_processor(m) == "hello world"


def test_str_processor_group() -> None:
    """Unit test for str_processor_group."""
    m = fullmatch(r"(?P<greeting>[a-z]+) ([a-z]+)", "hello world")
    assert m is not None
    assert str_processor_group(0)(m) == "hello world"
    assert str_processor_group("greeting")(m) == "hello"
    assert str_processor_group(1)(m) == "hello"
    assert str_processor_group(2)(m) == "world"
    with pytest.raises(IndexError, match=r"no such group"):
        int_processor_group(3)(m)
    with pytest.raises(IndexError, match=r"no such group"):
        int_processor_group("location")(m)


def test_str_tuple_processor() -> None:
    """Unit test for str_tuple_processor."""
    m = fullmatch(r"(.*) (.*) (.*)", "hello world again")
    assert m is not None
    assert str_tuple_processor(m) == ("hello", "world", "again")


def test_dataclass_processor() -> None:
    """Unit test for dataclass_processor."""

    @dataclass
    class TestDataClass:
        a: str
        b: int
        c: str
        d: int

    processor = dataclass_processor(TestDataClass)

    # test correct usage
    m = fullmatch(r"(?P<a>.*) (?P<b>.*) (?P<c>.*) (?P<d>.*)", "a 2 c -4")
    assert m is not None
    data = processor(m)
    assert data.a == "a"
    assert data.b == 2
    assert data.c == "c"
    assert data.d == -4

    # test with type mismatch
    m = fullmatch(r"(?P<a>.*) (?P<b>.*) (?P<c>.*) (?P<d>.*)", "a b c d")
    assert m is not None
    with pytest.raises(
        ValueError, match=r"invalid literal for int\(\) with base 10: 'b'"
    ):
        processor(m)

    # test with wrong field names
    m = fullmatch(r"(?P<x>.*) (?P<b>.*) (?P<c>.*) (?P<d>.*)", "a 2 c 4")
    assert m is not None
    with pytest.raises(
        TypeError, match=r"__init__\(\) missing 1 required positional argument: 'a'"
    ):
        processor(m)


def test_enum_processor() -> None:
    """Unit test for enum_processor."""

    class TestEnum(Enum):
        A = "A"
        B = "B"
        C = "C"

    processor = enum_processor(TestEnum)
    with pytest.raises(ValueError, match=r"argument must be subclass of Enum"):
        enum_processor(str)

    m = fullmatch(r".*", "B")
    assert m is not None
    assert processor(m) == TestEnum.B

    m = fullmatch(r".*", "D")
    assert m is not None
    with pytest.raises(
        ValueError, match=r"'D' is not a valid (test_enum_processor.<locals>.)?TestEnum"
    ):
        processor(m)


def test_validate_input_and_header() -> None:
    """Unit test for _validate_input_and_header."""
    puzzle_input = ["abc", "def", "ghi", "hkl"]

    # test with input too short
    with pytest.raises(ParseException):
        _validate_input_and_header([], 1, 4, ())

    # test with input too long
    with pytest.raises(ParseException):
        _validate_input_and_header(puzzle_input, 1, 1, ())

    # test without header
    assert _validate_input_and_header(puzzle_input, 1, 4, ()) == 0

    # test removing header
    assert _validate_input_and_header(puzzle_input, 1, 4, header=("abc", "def")) == 2

    # test removing wrong header
    with pytest.raises(ParseException):
        _validate_input_and_header(puzzle_input, 1, 4, header=("xyz",))


def test_parse_lines() -> None:
    """Unit test for parse_lines."""
    puzzle_input = ["abc", "def", "ghi", "hkl", "123"]

    # test with simple input
    assert parse_lines(puzzle_input, (r".*", str_processor)) == [
        "abc",
        "def",
        "ghi",
        "hkl",
        "123",
    ]

    # test with mixed input
    assert parse_lines(
        puzzle_input, (r"[a-z]*", str_processor), (r"[0-9]*", int_processor)
    ) == ["abc", "def", "ghi", "hkl", 123]

    # test with header
    assert parse_lines(puzzle_input, (r".*", str_processor), header=("abc", "def")) == [
        "ghi",
        "hkl",
        "123",
    ]

    # test with header
    assert parse_lines(puzzle_input, (r".*", str_processor), header=("abc", "def")) == [
        "ghi",
        "hkl",
        "123",
    ]

    # test with too short input
    with pytest.raises(ParseException):
        parse_lines(puzzle_input, (r".*", str_processor), min_length=10)

    # test with too long input
    with pytest.raises(ParseException):
        parse_lines(puzzle_input, (r".*", str_processor), max_length=1)

    # test with wrong type
    with pytest.raises(ParseException):
        parse_lines(puzzle_input, (r".*", int_processor))

    # test with no match
    with pytest.raises(ParseException):
        parse_lines(puzzle_input, (r"xyz", str_processor))


def test_parse_single_lines() -> None:
    """Unit test for parse_lines."""
    # test with simple input
    assert parse_single_line(["abc"], r".*", str_processor) == "abc"

    # test with too short input
    with pytest.raises(ParseException):
        parse_single_line([], r".*", str_processor)

    # test with too long input
    with pytest.raises(ParseException):
        parse_single_line(["abc", "def"], r".*", str_processor)

    # test with wrong type
    with pytest.raises(ParseException):
        parse_single_line(["abc"], r".*", int_processor)


def test_parse_tokens() -> None:
    """Unit tet for parse_tokens."""
    puzzle_input = ["a b c", "  1 2 3", "4 5 6", "7 8 9"]

    # test with good input
    assert parse_tokens(puzzle_input, (r"[a-z0-9]", str_processor), delimiter=" ") == [
        ["a", "b", "c"],
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]

    # test with good input and multiple match processors
    assert parse_tokens(
        puzzle_input,
        (r"[a-z]*", str_processor),
        (r"[0-9]*", int_processor),
        delimiter=" ",
    ) == [
        ["a", "b", "c"],
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    # test with header removed
    assert parse_tokens(
        puzzle_input, (r"\d", int_processor), delimiter=" ", header=("a b c",)
    ) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    # test with wrong delimiter
    with pytest.raises(ParseException):
        parse_tokens(puzzle_input, (r"[a-z0-9]", str_processor), delimiter=",")

    # test with wrong reg ex
    with pytest.raises(ParseException):
        parse_tokens(puzzle_input, (r"\d", str_processor), delimiter=" ")

    # test wrong type
    with pytest.raises(ParseException):
        parse_tokens(puzzle_input, (r"[a-z0-9]", int_processor), delimiter=" ")

    # test with too short
    with pytest.raises(ParseException):
        parse_tokens(
            puzzle_input, (r"[a-z0-9]+", str_processor), min_length=10, delimiter=" "
        )

    # test with too long
    with pytest.raises(ParseException):
        parse_tokens(
            puzzle_input, (r"[a-z0-9]+", str_processor), max_length=1, delimiter=" "
        )


def test_parse_grid() -> None:
    """Unit test for parse_grid."""
    puzzle_input = ["header", "123", "456", "789"]
    expected = {
        (0, 0): 1,
        (1, 0): 2,
        (2, 0): 3,
        (0, 1): 4,
        (1, 1): 5,
        (2, 1): 6,
        (0, 2): 7,
        (1, 2): 8,
        (2, 2): 9,
    }

    # test with good input
    assert parse_grid(puzzle_input[1:], r"[0-9]", int_processor) == expected

    # test with header removed
    assert (
        parse_grid(puzzle_input, r"[0-9]", int_processor, header=("header",))
        == expected
    )

    # test with wrong reg ex
    with pytest.raises(ParseException):
        parse_grid(puzzle_input, r"xyz", int_processor)

    # test with too short
    with pytest.raises(ParseException):
        parse_grid(puzzle_input, r"[0-9]", int_processor, min_length=10)

    # test with too long
    with pytest.raises(ParseException):
        parse_grid(puzzle_input, r"[0-9]", int_processor, max_length=1)
