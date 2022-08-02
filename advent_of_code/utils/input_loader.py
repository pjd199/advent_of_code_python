"""Load puzzle input form a file and strip the whitespace."""
from typing import List, Union


def load_puzzle_input_file(year: Union[int, str], day: Union[int, str]) -> List[str]:
    """Load the file, remove whitespace and return a list of strings.

    Args:
        year (int): the year to load
        day (int): the day to load

    Returns:
        List[str]: the lines of the file
    """
    return load_file(f"./puzzle_input/year{year}/day{day}.txt")


def load_file(filename: str) -> List[str]:
    """Load the file, remove whitespace and return a list of strings.

    Args:
        filename (str): the filename

    Returns:
        List[str]: the lines of the file
    """
    with open(filename) as file:
        lines = file.readlines()
        while len(lines) and lines[-1].strip() == "":
            del lines[-1]
        lines = [x.strip() for x in lines]
        return lines


def load_multi_line_string(content: str) -> List[str]:
    """Load the content, remove whitespace and return a list of strings.

    Args:
        content (str): the input content, include end of line characters

    Returns:
        List[str]: the lines of the file
    """
    lines = content.splitlines()
    while len(lines) and lines[-1].strip() == "":
        del lines[-1]
    lines = [x.strip() for x in lines]
    return lines
