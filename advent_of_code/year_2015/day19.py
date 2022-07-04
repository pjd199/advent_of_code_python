"""Solution for day 19 of Advent of Code 2015."""
from re import compile
from typing import List, Tuple

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if puzzle_input is None or len(puzzle_input) < 3:
            raise RuntimeError("Puzzle input is empty")

        if len(puzzle_input[0].strip()) == 0:
            raise RuntimeError("Parse input - puzzle starts with blank line")

        self.replacements = []
        pattern = compile(r"(?P<a>[a-zA-Z]+) => (?P<b>[a-zA-Z]+)")
        for i, line in enumerate(puzzle_input[:-2]):
            match = pattern.fullmatch(line)
            if match:
                self.replacements.append((match["a"], match["b"]))
            else:
                raise RuntimeError(f"Parse error on line {i + 1}: {line}")

        self.medication = puzzle_input[-1]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return len(self._replace(self.medication, self.replacements))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve part two by working back from the medicine to "e",
        # repeatedly finding the shortest next option of all the
        # possible replacements using min to find the shortest
        # string in a list
        steps = 0
        options = self._replace(self.medication, self.replacements, reverse=True)
        while options:
            options = self._replace(
                min(options, key=len), self.replacements, reverse=True
            )
            steps += 1
        return steps

    def _replace(
        self,
        molecule: str,
        replacement_list: List[Tuple[str, str]],
        reverse: bool = False,
    ) -> List[str]:
        """Create a list of all the possible new molecules.

        Args:
            molecule (str): the input molecule
            replacement_list (List[Tuple[str, str]]): list of replacements
            reverse (bool): if True, reverses the replacement_list.
                Defaults to False.

        Returns:
            List[str]: a list of all the possible replacements
        """
        results = set()
        for a, b in replacement_list:
            if reverse:
                a, b = b, a

            results.update(
                [
                    molecule[:i] + b + molecule[i + len(a) :]
                    for i in range(len(molecule))
                    if molecule[i : i + len(a)] == a
                ]
            )
        return list(results)
