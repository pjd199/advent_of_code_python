"""The top level interface for all the daily Solver classes."""
from abc import ABC, abstractmethod
from typing import List, Union


class SolverInterface(ABC):
    """Solver interface."""

    YEAR: int
    DAY: int
    TITLE: str

    @abstractmethod
    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the object, parse and validate the input.

        Args:
            puzzle_input (List[str]): _description_
        """

    @abstractmethod
    def solve_part_one(self) -> Union[int, str]:
        """Solve part one of the puzzle.

        Returns:
            Union[int, str]: the answer, as either a str or an int
        """

    @abstractmethod
    def solve_part_two(self) -> Union[int, str]:
        """Solve part two of the puzzle.

        Returns:
            Union[int, str]: the answer, as either a str or an int
        """

    def solve_all(self) -> Union[List[int], List[str], List[Union[int, str]]]:
        """Solve both parts of the puzzle.

        Returns:
            List[Union[int, str]]: the answers, as a list
        """
        return [self.solve_part_one(), self.solve_part_two()]
