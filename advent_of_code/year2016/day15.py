"""Solves the puzzle for Day 15 of Advent of Code 2016.

# Timing is Everything

https://adventofcode.com/2016/day/15

## Part One

The halls open into an interior plaza containing a large kinetic
sculpture. The sculpture is in a sealed enclosure and seems to involve a
set of identical spherical capsules that are carried to the top and
allowed to [bounce through the maze](https://youtu.be/IxDoO9oODOk?t=177)
of spinning pieces.

Part of the sculpture is even interactive! When a button is pressed, a
capsule is dropped and tries to fall through slots in a set of rotating
discs to finally go through a little hole at the bottom and come out of
the sculpture. If any of the slots aren't aligned with the capsule as it
passes, the capsule bounces off the disc and soars away. You feel
compelled to get one of those capsules.

The discs pause their motion each second and come in different sizes;
they seem to each have a fixed number of positions at which they stop.
You decide to call the position with the slot `0`, and count up for each
position it reaches next.

Furthermore, the discs are spaced out so that after you push the button,
one second elapses before the first disc is reached, and one second
elapses as the capsule passes from one disc to the one below it. So, if
you push the button at `time=100`, then the capsule reaches the top disc
at `time=101`, the second disc at `time=102`, the third disc at
`time=103`, and so on.

The button will only drop a capsule at an integer time - no fractional
seconds allowed.

For example, at `time=0`, suppose you see the following arrangement:

```
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.

```

If you press the button exactly at `time=0`, the capsule would start to
fall; it would reach the first disc at `time=1`. Since the first disc
was at position `4` at `time=0`, by `time=1` it has ticked one position
forward. As a five-position disc, the next position is `0`, and the
capsule falls through the slot.

Then, at `time=2`, the capsule reaches the second disc. The second disc
has ticked forward two positions at this point: it started at position
`1`, then continued to position `0`, and finally ended up at position
`1` again. Because there's only a slot at position `0`, the capsule
bounces away.

If, however, you wait until `time=5` to push the button, then when the
capsule reaches each disc, the first disc will have ticked forward `5+1
= 6` times (to position `0`), and the second disc will have ticked
forward `5+2 = 7` times (also to position `0`). In this case, the
capsule would fall through the discs and come out of the machine.

However, your situation has more than two discs; you've noted their
positions in your puzzle input. What is the *first time you can press
the button* to get a capsule?

## Part Two

After getting the first capsule (it contained a star! what great
fortune!), the machine detects your success and begins to rearrange
itself.

When it's done, the discs are back in their original configuration as if
it were `time=0` again, but a new disc with `11` positions and starting
at position `0` has appeared exactly one second below the
previously-bottom disc.

With this new disc, and counting again starting from `time=0` with the
configuration in your puzzle input, what is the *first time you can
press the button* to get another capsule?
"""
from dataclasses import dataclass
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Disc:
    """Stores disc data."""

    positions: int
    start: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 15
    TITLE = "Timing is Everything"

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
        self.discs = []
        pattern = compile(
            r"Disc #(?P<number>\d+) has (?P<positions>\d+) positions; "
            r"at time=0, it is at position (?P<start>\d+)."
        )
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.discs.append(Disc(int(m["positions"]), int(m["start"])))
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(self.discs)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(self.discs + [Disc(11, 0)])

    def _run(self, discs: List[Disc]) -> int:
        time = 0
        while any(
            (
                ((disc.start + time + t + 1) % disc.positions) != 0
                for t, disc in enumerate(discs)
            )
        ):
            time += 1

        return time


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
