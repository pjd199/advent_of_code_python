"""The top level interface for all the daily Solver classes."""
from abc import ABC, abstractmethod


class SolverInterface(ABC):
    """Solver interface."""

    YEAR: int
    DAY: int
    TITLE: str

    @abstractmethod
    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the object, parse and validate the input.

        Args:
            puzzle_input (list[str]): the puzzle input
        """

    @abstractmethod
    def solve_part_one(self) -> int | str:
        """Solve part one of the puzzle."""

    @abstractmethod
    def solve_part_two(self) -> int | str:
        """Solve part two of the puzzle."""
