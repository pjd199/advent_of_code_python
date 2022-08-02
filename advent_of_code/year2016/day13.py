"""Solves the puzzle for Day 13 of Advent of Code 2016.

# A Maze of Twisty Little Cubicles

https://adventofcode.com/2016/day/13

## Part One

You arrive at the first floor of this new building to discover a much
less welcoming environment than the shiny atrium of the last one.
Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative
integers (`x,y`). Each such coordinate is either a wall or an open
space. You can't move diagonally. The cube maze starts at `0,0` and
seems to extend infinitely toward *positive* `x` and `y`; negative
values are *invalid*, as they represent a location outside the building.
You are in a small waiting area at `1,1`.

While it seems chaotic, a nearby morale-boosting poster explains, the
layout is actually quite logical. You can determine whether a given
`x,y` coordinate will be a wall or an open space using a simple system:

* Find `x*x + 3*x + 2*x*y + y + y*y`.
* Add the office designer's favorite number (your puzzle input).
* Find the [binary representation](https://en.wikipedia.org/wiki/Binary_number)
  of that sum; count the *number* of [bits](https://en.wikipedia.org/wiki/Bit)
  that are `1`.
    + If the number of bits that are `1` is *even*, it's an *open space*.
    + If the number of bits that are `1` is *odd*, it's a *wall*.

For example, if the office designer's favorite number were `10`, drawing
walls as `#` and open spaces as `.`, the corner of the building
containing `0,0` would look like this:

```
  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

```

Now, suppose you wanted to reach `7,4`. The shortest route you could
take is marked as `O`:

```
  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

```

Thus, reaching `7,4` would take a minimum of `11` steps (starting from
your current location, `1,1`).

What is the *fewest number of steps required* for you to reach `31,39`?

## Part Two

<<<INSERT PART TWO HERE>>>
"""
from collections import deque
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 13
    TITLE = "A Maze of Twisty Little Cubicles"

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
        pattern = compile(r"\d+")
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.number = int(m[0])
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

        self.has_run = False

    def _open_space(self, x: int, y: int) -> bool:
        """Check to see if this location is open space.

        Args:
            x (int): x co-ordinate
            y (int): y co-ordinate

        Returns:
            bool: True is open space, else False
        """
        value = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + self.number
        return sum([1 for c in f"{value:b}" if c == "1"]) % 2 == 0

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.steps_to_target

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.within_50_steps

    def _run(self) -> None:
        """Run the simulation."""
        if self.has_run:
            return
        self.has_run = True

        target = (31, 39)

        queue = deque([(1, 1, 0)])
        visited = {(1, 1)}

        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        self.within_50_steps = 0
        self.steps_to_target = 0
        while queue:
            x, y, steps = queue.popleft()

            if (x, y) == target:
                self.steps_to_target = steps
                break

            if steps <= 50:
                self.within_50_steps += 1

            for move in moves:
                x1, y1 = x + move[0], y + move[1]
                if x1 >= 0 and y1 >= 0 and (x1, y1) not in visited:
                    visited.add((x1, y1))
                    if self._open_space(x1, y1):
                        queue.append((x1, y1, steps + 1))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
