"""Solves the puzzle for Day 13 of Advent of Code 2019.

Care Package

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/13
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 13
    TITLE = "Care Package"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.computer.reset()

        result = 0
        while (
            self.computer.execute(sleep_after_output=True)
            and self.computer.execute(sleep_after_output=True)
            and self.computer.execute(sleep_after_output=True)
        ):
            _, _, tile_id = tuple(self.computer.iterate_output())
            if tile_id == 2:
                result += 1

        return result

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self.computer.reset()

        # enable free play
        self.computer.memory[0] = 2

        # run the game, moving the paddle to follow with the ball
        ball_x = 0
        paddle_x = 0
        score = 0
        while (
            self.computer.execute(sleep_after_output=True)
            and self.computer.execute(sleep_after_output=True)
            and self.computer.execute(sleep_after_output=True)
        ):
            x, y, tile_id = tuple(self.computer.iterate_output())

            if x == -1 and y == 0:
                score = tile_id
            elif tile_id == 3:
                paddle_x = x
            elif tile_id == 4:
                ball_x = x
                joystick = 1 if ball_x > paddle_x else -1 if ball_x < paddle_x else 0
                self.computer.input_data(joystick)

        return score


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
