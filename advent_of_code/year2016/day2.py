"""Solves the puzzle for Day 2 of Advent of Code 2016."""

from typing import Dict, List, Tuple

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        self.input = []
        for line in puzzle_input:
            if all([c in ["U", "D", "L", "R"] for c in line]):
                self.input.append(line)
            else:
                raise RuntimeError(
                    f"Puzzle input should only contain 'U', 'D', 'L' or 'R', "
                    f"found {puzzle_input[0]}"
                )

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return self._find_code(
            {
                (0, 0): "1",
                (1, 0): "2",
                (2, 0): "3",
                (0, 1): "4",
                (1, 1): "5",
                (2, 1): "6",
                (0, 2): "7",
                (1, 2): "8",
                (2, 2): "9",
            }
        )

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return self._find_code(
            {
                (2, 0): "1",
                (1, 1): "2",
                (2, 1): "3",
                (3, 1): "4",
                (0, 2): "5",
                (1, 2): "6",
                (2, 2): "7",
                (3, 2): "8",
                (4, 2): "9",
                (1, 3): "A",
                (2, 3): "B",
                (3, 3): "D",
                (2, 4): "D",
            }
        )

    def _find_code(self, grid: Dict[Tuple[int, int], str]) -> str:
        """Find the code, starting at "5".

        Args:
            grid (Dict[Tuple[int, int], str]): keypad mapping (x, y),
                where (0, 0) is top left

        Returns:
            str: the code
        """
        # find the starting point at "5"
        inverse_grid = {v: k for k, v in grid.items()}
        x, y = inverse_grid["5"]

        # find the code
        code = []
        for line in self.input:
            for c in line:
                if c == "U" and (x, y - 1) in grid:
                    y -= 1
                elif c == "D" and (x, y + 1) in grid:
                    y += 1
                elif c == "L" and (x - 1, y) in grid:
                    x -= 1
                elif c == "R" and (x + 1, y) in grid:
                    x += 1
            code.append(grid[(x, y)])

        return "".join(code)
