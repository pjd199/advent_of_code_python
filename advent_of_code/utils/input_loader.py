"""Load puzzle input form a file and strip the whitespace."""
from typing import List


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
