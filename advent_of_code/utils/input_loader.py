"""Load puzzle input form a file and strip the whitespace."""
from pathlib import Path


def load_puzzle_input_file(year: int | str, day: int | str) -> list[str]:
    """Load the file, remove whitespace and return a list of strings.

    Args:
        year (int | str): the year to load
        day (int | str): the day to load

    Returns:
        list[str]: the lines of the file
    """
    return load_file(f"./puzzle_input/year{year}/day{day}.txt")


def load_file(filename: str) -> list[str]:
    """Load the file, remove whitespace and return a list of strings.

    Args:
        filename (str): the filename

    Returns:
        list[str]: the lines of the file
    """
    with Path(filename).open() as file:
        lines = file.readlines()
        while len(lines) and lines[-1].strip() == "":
            del lines[-1]
        return [x.rstrip("\n") for x in lines]


def load_multi_line_string(content: str) -> list[str]:
    """Load the content, remove whitespace and return a list of strings.

    Args:
        content (str): the input content, include end of line characters

    Returns:
        list[str]: the lines of the file
    """
    lines = content.splitlines()
    while len(lines) and lines[-1].strip() == "":
        del lines[-1]
    return lines
