"""Solves the puzzle for Day 18 of Advent of Code 2016.

# Like a Rogue

https://adventofcode.com/2016/day/18

## Part One

As you enter this room, you hear a loud click! Some of the tiles in the
floor here seem to be pressure plates for
[traps](https://nethackwiki.com/wiki/Trap), and the trap you just
triggered has run out of... whatever it tried to do to you. You doubt
you'll be so lucky next time.

Upon closer examination, the traps and safe tiles in this room seem to
follow a pattern. The tiles are arranged into rows that are all the same
width; you take note of the safe tiles (`.`) and traps (`^`) in the
first row (your puzzle input).

The type of tile (trapped or safe) in each row is based on the types of
the tiles in the same position, and to either side of that position, in
the previous row. (If either side is off either end of the row, it
counts as 'safe' because there isn't a trap embedded in the wall.)

For example, suppose you know the first row (with tiles marked by
letters) and want to determine the next row (with tiles marked by
numbers):

```
ABCDE
12345

```

The type of tile `2` is based on the types of tiles `A`, `B`, and `C`;
the type of tile `5` is based on tiles `D`, `E`, and an imaginary 'safe'
tile. Let's call these three tiles from the previous row the *left*,
*center*, and *right* tiles, respectively. Then, a new tile is a *trap*
only in one of the following situations:

* Its *left* and *center* tiles are traps, but its *right* tile is not.
* Its *center* and *right* tiles are traps, but its *left* tile is not.
* Only its *left* tile is a trap.
* Only its *right* tile is a trap.

In any other situation, the new tile is safe.

Then, starting with the row `..^^.`, you can determine the next row by
applying those rules to each new tile:

* The leftmost character on the next row considers the left (nonexistent, so
  we assume 'safe'), center (the first `.`, which means 'safe'), and right (the
  second `.`, also 'safe') tiles on the previous row. Because all of the trap
  rules require a trap in at least one of the previous three tiles, the first
  tile on this new row is also safe, `.`.
* The second character on the next row considers its left (`.`), center (`.`),
  and right (`^`) tiles from the previous row. This matches the fourth rule:
  only the right tile is a trap. Therefore, the next tile in this new row
  is a trap, `^`.
* The third character considers `.^^`, which matches the second trap rule:
  its center and right tiles are traps, but its left tile is not. Therefore,
  this tile is also a trap, `^`.
* The last two characters in this new row match the first and third rules,
  respectively, and so they are both also traps, `^`.

After these steps, we now know the next row of tiles in the room:
`.^^^^`. Then, we continue on to the next row, using the same rules, and
get `^^..^`. After determining two new rows, our map looks like this:

```
..^^.
.^^^^
^^..^

```

Here's a larger example with ten tiles per row and ten rows:

```
.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^

```

In ten rows, this larger example has `38` safe tiles.

Starting with the map in your puzzle input, in a total of `40` rows
(including the starting row), *how many safe tiles* are there?

## Part Two

*How many safe tiles* are there in a total of `400000` rows?
"""
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
    DAY = 18
    TITLE = "Like a Rogue"

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
        pattern = compile(r"[\.\^]+")
        for i, line in enumerate(puzzle_input):
            if (m := pattern.fullmatch(line)) and (i == 0):
                self.input = m[0]
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(40)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(400000)

    def _run(self, rows: int) -> int:
        """Run the simulation.

        Mapping the "^" to True, the 4 rules reduce reduce to left != right

        Args:
            rows (int): the number of rows

        Returns:
            int: the total number of safe / "." / False
        """
        traps = 0
        row = [x == "^" for x in self.input]
        for _ in range(rows):
            traps += row.count(True)
            row = [
                left != right for left, right in zip([False] + row, row[1:] + [False])
            ]
        return (len(row) * rows) - traps


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
