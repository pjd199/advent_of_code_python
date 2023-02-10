"""Tests for Advent of Code ASCII art.

Forked from https://github.com/bsoyka/advent-of-code-ocr 0.2.0, under MIT License.
"""
from itertools import chain
from typing import Set, Tuple

import numpy as np
import pytest

from advent_of_code.utils.ocr import (
    ALPHABET_6,
    ALPHABET_10,
    ocr_coordinates,
    ocr_numpy,
    ocr_sequence,
)


@pytest.mark.parametrize(
    ("test_input", "expected"), chain(ALPHABET_6.items(), ALPHABET_10.items())
)
def test_single_letter(test_input: str, expected: str) -> None:
    """Test that all the letters can be read.

    Args:
        test_input (str): the input array
        expected (str): the expected result
    """
    assert ocr_sequence(test_input.splitlines()) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"), chain(ALPHABET_6.items(), ALPHABET_10.items())
)
def test_coordinates(test_input: str, expected: str) -> None:
    """Test that all the letters can be read.

    Args:
        test_input (str): the input array
        expected (str): the expected result
    """
    array = test_input.splitlines()
    coordinates = {
        (x, y)
        for y in range(len(array))
        for x in range(len(array[0]))
        if array[y][x] == "#"
    }
    assert ocr_coordinates(coordinates) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (
            """.##..###...##.
#..#.#..#.#..#
#..#.###..#...
####.#..#.#...
#..#.#..#.#..#
#..#.###...##.""",
            "ABC",
        ),
        (
            """######..######...####.
#.......#.......#....#
#.......#.......#.....
#.......#.......#.....
#####...#####...#.....
#.......#.......#..###
#.......#.......#....#
#.......#.......#....#
#.......#.......#...##
######..#........###.#""",
            "EFG",
        ),
    ],
)
def test_three_letters(test_input: str, expected: str) -> None:
    """Test that all the letters can be read.

    Args:
        test_input (str): the input array
        expected (str): the expected result
    """
    assert ocr_sequence(test_input.splitlines()) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (
            {
                (3, 4),
                (3, 1),
                (5, 4),
                (5, 1),
                (0, 2),
                (8, 3),
                (0, 5),
                (11, 5),
                (1, 0),
                (10, 3),
                (1, 3),
                (6, 2),
                (6, 5),
                (12, 0),
                (3, 3),
                (5, 0),
                (5, 3),
                (10, 2),
                (0, 1),
                (13, 4),
                (0, 4),
                (13, 1),
                (7, 0),
                (12, 5),
                (3, 2),
                (3, 5),
                (5, 2),
                (5, 5),
                (8, 4),
                (8, 1),
                (11, 0),
                (10, 4),
                (0, 3),
                (2, 0),
                (10, 1),
                (2, 3),
                (7, 2),
                (6, 0),
                (7, 5),
            },
            "ABC",
        ),
        (
            {
                (5, 4),
                (5, 1),
                (8, 0),
                (0, 2),
                (0, 5),
                (2, 2),
                (1, 0),
                (11, 5),
                (10, 3),
                (2, 5),
                (13, 5),
                (6, 2),
                (12, 0),
                (12, 3),
                (3, 0),
                (5, 0),
                (5, 3),
                (10, 2),
                (0, 1),
                (1, 2),
                (0, 4),
                (13, 4),
                (13, 1),
                (1, 5),
                (7, 0),
                (12, 5),
                (3, 5),
                (5, 2),
                (5, 5),
                (0, 0),
                (11, 0),
                (10, 4),
                (0, 3),
                (2, 0),
                (10, 1),
                (13, 3),
                (7, 2),
                (6, 0),
            },
            "EFG",
        ),
        (
            {
                (12, 4),
                (2, 4),
                (10, 5),
                (12, 1),
                (2, 1),
                (1, 5),
                (5, 4),
                (7, 0),
                (8, 0),
                (8, 3),
                (11, 2),
                (10, 0),
                (2, 2),
                (1, 0),
                (10, 3),
                (2, 5),
                (13, 5),
                (3, 5),
                (8, 4),
                (6, 5),
                (8, 1),
                (10, 4),
                (2, 0),
                (10, 1),
                (13, 0),
                (3, 0),
                (2, 3),
                (12, 3),
                (8, 2),
                (7, 5),
                (10, 2),
            },
            "IJK",
        ),
        (
            {
                (12, 4),
                (17, 0),
                (5, 4),
                (5, 7),
                (8, 0),
                (19, 0),
                (17, 9),
                (0, 2),
                (8, 3),
                (10, 0),
                (8, 9),
                (0, 5),
                (8, 6),
                (13, 2),
                (10, 9),
                (0, 8),
                (2, 5),
                (13, 5),
                (9, 9),
                (16, 4),
                (16, 1),
                (13, 8),
                (16, 7),
                (19, 9),
                (12, 0),
                (3, 0),
                (12, 9),
                (4, 5),
                (5, 6),
                (5, 3),
                (5, 9),
                (8, 2),
                (8, 5),
                (11, 4),
                (9, 4),
                (0, 7),
                (8, 8),
                (0, 4),
                (13, 1),
                (1, 5),
                (13, 7),
                (16, 3),
                (18, 0),
                (16, 6),
                (18, 9),
                (20, 0),
                (20, 9),
                (21, 8),
                (4, 1),
                (3, 5),
                (5, 2),
                (9, 0),
                (5, 5),
                (8, 4),
                (5, 8),
                (11, 0),
                (8, 1),
                (1, 1),
                (0, 3),
                (2, 0),
                (0, 9),
                (10, 4),
                (0, 6),
                (8, 7),
                (11, 9),
                (13, 3),
                (16, 2),
                (13, 6),
                (16, 5),
                (16, 8),
                (21, 1),
            },
            "ABC",
        ),
        (
            {
                (4, 0),
                (12, 7),
                (3, 4),
                (17, 0),
                (4, 6),
                (5, 1),
                (9, 2),
                (8, 0),
                (19, 0),
                (17, 9),
                (0, 2),
                (8, 9),
                (17, 6),
                (19, 9),
                (0, 5),
                (11, 5),
                (1, 0),
                (0, 8),
                (13, 8),
                (16, 7),
                (21, 0),
                (21, 9),
                (12, 3),
                (3, 0),
                (12, 6),
                (5, 3),
                (5, 9),
                (9, 7),
                (11, 4),
                (0, 1),
                (0, 7),
                (2, 4),
                (8, 8),
                (0, 4),
                (10, 5),
                (13, 1),
                (16, 0),
                (18, 0),
                (16, 9),
                (21, 2),
                (20, 0),
                (18, 9),
                (12, 2),
                (20, 3),
                (20, 9),
                (4, 7),
                (3, 5),
                (5, 2),
                (4, 4),
                (19, 4),
                (9, 3),
                (0, 0),
                (5, 8),
                (8, 1),
                (10, 4),
                (0, 3),
                (2, 0),
                (0, 9),
                (1, 4),
                (0, 6),
                (9, 6),
                (13, 0),
                (13, 9),
                (16, 8),
                (18, 5),
                (21, 1),
            },
            "RXZ",
        ),
    ],
)
def test_coordinates_three_letters(
    test_input: Set[Tuple[int, int]], expected: str
) -> None:
    """Test that all the letters can be read.

    Args:
        test_input (Set[Tuple[int,int]]): the input array
        expected (str): the expected result
    """
    assert ocr_coordinates(test_input) == expected


@pytest.mark.parametrize(
    ("test_input", "fill_char", "empty_char", "expected"),
    [
        (
            "abbaabbbaaabba\n"
            "baababaababaab\n"
            "baababbbaabaaa\n"
            "bbbbabaababaaa\n"
            "baababaababaab\n"
            "baababbbaaabba",
            "b",
            "a",
            "ABC",
        ),
        (
            "!@@!!@@@!!!@@!\n"
            "@!!@!@!!@!@!!@\n"
            "@!!@!@@@!!@!!!\n"
            "@@@@!@!!@!@!!!\n"
            "@!!@!@!!@!@!!@\n"
            "@!!@!@@@!!!@@!",
            "@",
            "!",
            "ABC",
        ),
    ],
)
def test_different_characters(
    test_input: str, fill_char: str, empty_char: str, expected: str
) -> None:
    """Test that all the letters can be read.

    Args:
        test_input (str): the input array
        fill_char(str): the fill character
        empty_char(str): the empty character
        expected(str): the expected result
    """
    assert (
        ocr_sequence(
            test_input.splitlines(), fill_pixel=fill_char, empty_pixel=empty_char
        )
        == expected
    )


def test_long_string() -> None:
    """Test a longer input string."""
    string = (
        ".##..###...##..####.####..##..#..#..###...##."
        "#..#.#.....##..###..###...###.#..#.#...#####\n"
        "#..#.#..#.#..#.#....#....#..#.#..#...#.....#."
        "#.#..#....#..#.#..#.#..#.#....#..#.#...#...#\n"
        "#..#.###..#....###..###..#....####...#.....#."
        "##...#....#..#.#..#.#..#.#....#..#..#.#...#.\n"
        "####.#..#.#....#....#....#.##.#..#...#.....#."
        "#.#..#....#..#.###..###...##..#..#...#...#..\n"
        "#..#.#..#.#..#.#....#....#..#.#..#...#..#..#."
        "#.#..#....#..#.#....#.#.....#.#..#...#..#...\n"
        "#..#.###...##..####.#.....###.#..#..###..##.."
        "#..#.####..##..#....#..#.###...##....#..####"
    )
    assert ocr_sequence(string.splitlines()) == "ABCEFGHIJKLOPRSUYZ"


@pytest.mark.parametrize("rows", [0, 1, 5, 7, 9, 11])
def test_number_of_rows(rows: int) -> None:
    """Test processing for the wrong number of rows.

    Args:
        rows (int): number of rows
    """
    with pytest.raises(
        ValueError, match=r"incorrect number of rows \(expected 6 or 10\)"
    ):
        ocr_sequence("\n".join("test" for _ in range(rows)))


@pytest.mark.parametrize(("rows", "cols"), [(6, 6), (6, 12), (10, 16), (10, 32)])
def test_number_of_cols(rows: int, cols: int) -> None:
    """Test processing for the wrong number of rows.

    Args:
        rows (int): number of rows
        cols (int): number of columns
    """
    array = [["." for _ in range(cols)] for row in range(rows)]
    array[-1].append(".")

    with pytest.raises(
        ValueError, match="all rows should have the same number of columns"
    ):
        ocr_sequence(array)


def test_sequence_nested_list() -> None:
    """Test parsing a nested array."""
    array = [
        ["X", "O", "O", "X", "X", "X", "O", "O", "X"],
        ["O", "X", "X", "O", "X", "O", "X", "X", "O"],
        ["O", "X", "X", "O", "X", "O", "X", "X", "X"],
        ["O", "O", "O", "O", "X", "O", "X", "X", "X"],
        ["O", "X", "X", "O", "X", "O", "X", "X", "O"],
        ["O", "X", "X", "O", "X", "X", "O", "O", "X"],
    ]
    assert ocr_sequence(array, fill_pixel="O", empty_pixel="X") == "AC"


def test_numpy() -> None:
    """Test parsing a numpy array."""
    array = np.array(
        [
            ["X", "O", "O", "X", "X", "X", "O", "O", "X"],
            ["O", "X", "X", "O", "X", "O", "X", "X", "O"],
            ["O", "X", "X", "O", "X", "O", "X", "X", "X"],
            ["O", "O", "O", "O", "X", "O", "X", "X", "X"],
            ["O", "X", "X", "O", "X", "O", "X", "X", "O"],
            ["O", "X", "X", "O", "X", "X", "O", "O", "X"],
        ]
    )
    assert ocr_numpy(array, fill_pixel="O", empty_pixel="X") == "AC"
