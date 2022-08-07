"""Solves the puzzle for Day 19 of Advent of Code 2016.

# An Elephant Named Joseph

https://adventofcode.com/2016/day/19

## Part One

The Elves contact you over a highly secure emergency channel. Back at
the North Pole, the Elves are busy misunderstanding [White Elephant
parties](https://en.wikipedia.org/wiki/White_elephant_gift_exchange).

Each Elf brings a present. They all sit in a circle, numbered starting
with position `1`. Then, starting with the first Elf, they take turns
stealing all the presents from the Elf to their left. An Elf with no
presents is removed from the circle and does not take turns.

For example, with five Elves (numbered `1` to `5`):

```
  1
5   2
 4 3

```

* Elf `1` takes Elf `2`'s present.
* Elf `2` has no presents and is skipped.
* Elf `3` takes Elf `4`'s present.
* Elf `4` has no presents and is also skipped.
* Elf `5` takes Elf `1`'s two presents.
* Neither Elf `1` nor Elf `2` have any presents, so both are skipped.
* Elf `3` takes Elf `5`'s three presents.

So, with *five* Elves, the Elf that sits starting in position `3` gets
all the presents.

With the number of Elves given in your puzzle input, *which Elf gets all
the presents?*

## Part Two

Realizing the folly of their present-exchange rules, the Elves agree to
instead steal presents from the Elf *directly across the circle*. If two
Elves are across the circle, the one on the left (from the perspective
of the stealer) is stolen from. The other rules remain unchanged: Elves
with no presents are removed from the circle entirely, and the other
elves move in slightly to keep the circle evenly spaced.

For example, with five Elves (again numbered `1` to `5`):

* The Elves sit in a circle; Elf `1` goes first:

```
  *1*
5   2
 4 3

```
* Elves `3` and `4` are across the circle; Elf `3`'s present is stolen,
  being the one to the left. Elf `3` leaves the circle, and the rest of
  the Elves move in:

```
  *1*           1
5   2  -->  5   2
 4 -          4

```
* Elf `2` steals from the Elf directly across the circle, Elf `5`:

```
  1         1
-   *2*  -->     2
  4         4

```
* Next is Elf `4` who, choosing between Elves `1` and `2`, steals from Elf `1`:

```
 -          2
    2  -->
 *4*          4

```
* Finally, Elf `2` steals from Elf `4`:

```
 *2*
    -->  2
 -

```

So, with *five* Elves, the Elf that sits starting in position `2` gets
all the presents.

With the number of Elves given in your puzzle input, *which Elf now gets
all the presents?*
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
    DAY = 19
    TITLE = "An Elephant Named Joseph"

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
            if (m := pattern.fullmatch(line)) and (i == 0):
                self.number_of_elves = int(m[0])
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

            running mathmatical solution for "Josephus problem"
            https://en.wikipedia.org/wiki/Josephus_problem

        Returns:
            int: the answer
        """
        exponent = 1
        while (2 ** int(exponent + 1)) <= self.number_of_elves:
            exponent += 1
        return 2 * (self.number_of_elves - int(2**exponent)) + 1

    def solve_part_two(self) -> int:  # pragma: no cover
        """Solve part two of the puzzle.

            Following the mathmatical solution to part one,
            this formula was developed by observing the pattern
            for first 100 numbers

        Returns:
            int: the answer
        """
        exponent = 1
        while (3 ** int(exponent + 1)) <= self.number_of_elves:
            exponent += 1

        if self.number_of_elves < 3:
            return 1
        else:
            if self.number_of_elves > (2 * int(3**exponent)):
                return (2 * self.number_of_elves) - int(3 ** (exponent + 1))
            else:
                return self.number_of_elves - int(3**exponent)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
