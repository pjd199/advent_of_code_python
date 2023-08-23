"""Convert Advent of Code ASCII art.

Forked from https://github.com/bsoyka/advent-of-code-ocr 0.2.0, under MIT License.

"""
from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike


class OcrError(Exception):
    """Error."""

    ROW = "Incorrect number of rows (expected 6 or 10)"
    COL = "All rows should have the same number of columns"
    INVALID = "Unable to OCR input"


def ocr_coordinates(coordinates: set[tuple[int, int]]) -> str:
    """Convert a set of co-ordinates into letters.

    Args:
        coordinates (set[tuple[int, int]]): the (x,y) pixels of the text

    Returns:
        str: the OCR'd word
    """
    (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*coordinates))

    # workaround for words starting which 'i', which is three characters wide
    width = max_x + 1 - min_x
    height = max_y + 1 - min_y
    if (height == 6 and (width + 1) % 5 != 0) or (height == 8 and (width + 1) % 8 != 0):
        min_x -= 1

    return ocr_sequence(
        [
            ["#" if (x, y) in coordinates else "." for x in range(min_x, max_x + 1)]
            for y in range(min_y, max_y + 1)
        ]
    )


def ocr_numpy(
    array: ArrayLike,
    fill_pixel: str | int | bool = "#",
    empty_pixel: str | int | bool = ".",
) -> str:
    """Convert an array of pixels into letters.

    Args:
        array (ArrayLike): the input array
        fill_pixel (str | int | bool): the filled pixel. Defaults to "#".
        empty_pixel (str | int | bool): the empty pixel. Defaults to ".".

    Returns:
        str: the result
    """
    return ocr_sequence(np.array(array).tolist(), fill_pixel, empty_pixel)


def ocr_sequence(
    array: Sequence[Sequence[str | int | bool]],
    fill_pixel: str | int | bool = "#",
    empty_pixel: str | int | bool = ".",
) -> str:
    """Convert an array of pixels into letters.

    Args:
        array (Sequence[Sequence[str | int | bool]]): the input array
        fill_pixel (str | int | bool): the filled pixel. Defaults to "#".
        empty_pixel (str | int | bool): the empty pixel. Defaults to ".".

    Raises:
        ValueError: Raised if the wrong number of rows are found
        ValueError: Raised if the columns are not all equal length

    Returns:
        str: the result
    """
    prepared_array = [
        [
            "#" if pixel == fill_pixel else "." if pixel == empty_pixel else ""
            for pixel in line
        ]
        for line in array
    ]

    # prepare the settings for 6 or 10 rows
    rows = len(prepared_array)
    if rows == 6:
        alphabet = ALPHABET_6
        width = 4
        padding = 1
    elif rows == 10:
        alphabet = ALPHABET_10
        width = 6
        padding = 2
    else:
        raise OcrError(OcrError.ROW)

    cols = len(prepared_array[0])

    if any(len(row) != cols for row in prepared_array):
        raise OcrError(OcrError.COL)

    # Convert each letter
    try:
        indices = [
            slice(start, start + width) for start in range(0, cols, width + padding)
        ]
        result = [
            alphabet["\n".join("".join(row[index]) for row in prepared_array)]
            for index in indices
        ]
    except KeyError as e:
        raise OcrError(OcrError.INVALID) from e

    return "".join(result)


ALPHABET_6 = {
    ".##.\n#..#\n#..#\n####\n#..#\n#..#": "A",
    "###.\n#..#\n###.\n#..#\n#..#\n###.": "B",
    ".##.\n#..#\n#...\n#...\n#..#\n.##.": "C",
    "####\n#...\n###.\n#...\n#...\n####": "E",
    "####\n#...\n###.\n#...\n#...\n#...": "F",
    ".##.\n#..#\n#...\n#.##\n#..#\n.###": "G",
    "#..#\n#..#\n####\n#..#\n#..#\n#..#": "H",
    ".###\n..#.\n..#.\n..#.\n..#.\n.###": "I",
    "..##\n...#\n...#\n...#\n#..#\n.##.": "J",
    "#..#\n#.#.\n##..\n#.#.\n#.#.\n#..#": "K",
    "#...\n#...\n#...\n#...\n#...\n####": "L",
    ".##.\n#..#\n#..#\n#..#\n#..#\n.##.": "O",
    "###.\n#..#\n#..#\n###.\n#...\n#...": "P",
    "###.\n#..#\n#..#\n###.\n#.#.\n#..#": "R",
    ".###\n#...\n#...\n.##.\n...#\n###.": "S",
    "#..#\n#..#\n#..#\n#..#\n#..#\n.##.": "U",
    "#...\n#...\n.#.#\n..#.\n..#.\n..#.": "Y",
    "####\n...#\n..#.\n.#..\n#...\n####": "Z",
}

ALPHABET_10 = {
    """..##..
.#..#.
#....#
#....#
#....#
######
#....#
#....#
#....#
#....#""": "A",
    """#####.
#....#
#....#
#....#
#####.
#....#
#....#
#....#
#....#
#####.""": "B",
    """.####.
#....#
#.....
#.....
#.....
#.....
#.....
#.....
#....#
.####.""": "C",
    """######
#.....
#.....
#.....
#####.
#.....
#.....
#.....
#.....
######""": "E",
    """######
#.....
#.....
#.....
#####.
#.....
#.....
#.....
#.....
#.....""": "F",
    """.####.
#....#
#.....
#.....
#.....
#..###
#....#
#....#
#...##
.###.#""": "G",
    """#....#
#....#
#....#
#....#
######
#....#
#....#
#....#
#....#
#....#""": "H",
    """...###
....#.
....#.
....#.
....#.
....#.
....#.
#...#.
#...#.
.###..""": "J",
    """#....#
#...#.
#..#..
#.#...
##....
##....
#.#...
#..#..
#...#.
#....#""": "K",
    """#.....
#.....
#.....
#.....
#.....
#.....
#.....
#.....
#.....
######""": "L",
    """#....#
##...#
##...#
#.#..#
#.#..#
#..#.#
#..#.#
#...##
#...##
#....#""": "N",
    """#####.
#....#
#....#
#....#
#####.
#.....
#.....
#.....
#.....
#.....""": "P",
    """#####.
#....#
#....#
#....#
#####.
#..#..
#...#.
#...#.
#....#
#....#""": "R",
    """#....#
#....#
.#..#.
.#..#.
..##..
..##..
.#..#.
.#..#.
#....#
#....#""": "X",
    """######
.....#
.....#
....#.
...#..
..#...
.#....
#.....
#.....
######""": "Z",
}
