"""Solves the puzzle for Day 7 of Advent of Code 2015.

Some Assembly Required

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/7
"""
from copy import deepcopy
from pathlib import Path
from re import compile
from sys import path
from typing import Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 7
    TITLE = "Some Assembly Required"

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

        self.wiring_diagram = {}
        pattern = compile(
            r"((?P<signal>[0-9]+)"
            r"|(?P<input_wire>[a-z]+)"
            r"|(?P<left_operand>[a-z]*|[0-9]*)\s?"
            r"(?P<operator>AND|OR|LSHIFT|RSHIFT|NOT) "
            r"(?P<right_operand>[a-z]*|[0-9]*))"
            r" -> (?P<output_wire>[a-z]+)"
        )
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                self.wiring_diagram[match["output_wire"]] = match.groupdict()
            else:
                raise RuntimeError(f"Parse error at line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._resolve("a", self.wiring_diagram, {})

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        md = deepcopy(self.wiring_diagram)
        md["b"]["signal"] = str(self._resolve("a", self.wiring_diagram, {}))
        return self._resolve("a", md, {})

    def solve_all(self) -> List[int]:
        """Solve both parts.

        Returns:
            List[int]: the results of part one and part two
        """
        part_one = self._resolve("a", self.wiring_diagram, {})
        md = deepcopy(self.wiring_diagram)
        md["b"]["signal"] = str(part_one)
        part_two = self._resolve("a", md, {})

        return [part_one, part_two]

    def _resolve(
        self,
        wire: str,
        wiring_diagram: Dict[str, Dict[str, str]],
        cache: Dict[str, int],
    ) -> int:
        """Recursively resolves the signal on the request wire.

        Resolves the signal on the request wire, recursively nagivating the
        wiring_diagram to evaluate all the expressions. Uses a cache so that
        each expression is only evaluated once, minimising recursions

        Args:
            wire (str): the wire to resolve
            wiring_diagram (Dict[str, Dict[str,str]]): the wire inputs
            cache (Dict[str, int]): a cache of resolved results

        Returns:
            int: the final value of the wire
        """
        # if this is just a simple number, return the number as an int
        if isinstance(wire, str) and wire.isnumeric():
            return int(wire)

        # if this is not yet been cached, resolved the expression
        if wire not in cache:
            expression = wiring_diagram[wire]
            if expression["signal"] is not None:
                # signal source
                cache[wire] = int(expression["signal"])
            elif expression["input_wire"] is not None:
                # passthrough the wire value
                cache[wire] = self._resolve(
                    expression["input_wire"], wiring_diagram, cache
                )
            elif expression["operator"] == "AND":
                # AND the operands
                cache[wire] = self._resolve(
                    expression["left_operand"], wiring_diagram, cache
                ) & self._resolve(expression["right_operand"], wiring_diagram, cache)
            elif expression["operator"] == "OR":
                # OR the operands
                cache[wire] = self._resolve(
                    expression["left_operand"], wiring_diagram, cache
                ) | self._resolve(expression["right_operand"], wiring_diagram, cache)
            elif expression["operator"] == "LSHIFT":
                # LSHIFT the operand
                cache[wire] = self._resolve(
                    expression["left_operand"], wiring_diagram, cache
                ) << int(expression["right_operand"])
            elif expression["operator"] == "RSHIFT":
                # RSHIFT the operand
                cache[wire] = self._resolve(
                    expression["left_operand"], wiring_diagram, cache
                ) >> int(expression["right_operand"])
            elif expression["operator"] == "NOT":
                # NOT the operand
                cache[wire] = ~self._resolve(
                    expression["right_operand"], wiring_diagram, cache
                )

        # return the resolved value
        return cache[wire]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
