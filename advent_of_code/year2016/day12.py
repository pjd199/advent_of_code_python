"""Solves the puzzle for Day 12 of Advent of Code 2016.

--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted glass
ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some [tiger
lilies](https://www.google.com/search?q=tiger+lilies&tbm=isch), you manage to
decrypt some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building - it's a
collection of buildings in the nearby area. They're all connected by a local
monorail, and there's another building not far from here! Unfortunately, being
night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that the boot
sequence expects a password. The password-checking logic (your puzzle input) is
easy to extract, but the code it uses is strange: it's assembunny code designed
for the [new computer](11) you just assembled. You'll have to execute the code
and get the password.

The assembunny code you've extracted operates on four
[registers](https://en.wikipedia.org/wiki/Processor_register) (`a`, `b`, `c`,
and `d`) that start at `0` and can hold any
[integer](https://en.wikipedia.org/wiki/Integer). However, it seems to make use
of only a few [instructions](https://en.wikipedia.org/wiki/Instruction_set):

* `cpy x y` *copies* `x` (either an integer or the *value* of a register) into
    register `y`.
* `inc x` *increases* the value of register `x` by one.
* `dec x` *decreases* the value of register `x` by one.
* `jnz x y` *jumps* to an instruction `y` away (positive means forward; negative
    means backward), but only if `x` is *not zero*.

The `jnz` instruction moves relative to itself: an offset of `-1` would continue
at the previous instruction, while an offset of `2` would *skip over* the next
instruction.

For example:

```
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

```

The above code would set register `a` to `41`, increase its value by `2`,
decrease its value by `1`, and then skip the last `dec a` (because `a` is not
zero, so the `jnz a 2` skips it), leaving register `a` at `42`. When you move
past the last instruction, the program halts.

After executing the assembunny code in your puzzle input, *what value is left in
register `a`?*

--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't start;
register `c` needs to be initialized to the position of the ignition key.

If you instead *initialize register `c` to be `1`*, what value is now left in
register `a`?

Puzzle description from https://adventofcode.com/2016/day/12
"""
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":
    path.append(str(Path(__file__).parent.parent.parent))  # pragma: no cover

from advent_of_code.utils.input_loader import load_puzzle_input_file
from advent_of_code.utils.solver_interface import SolverInterface


class Action(Enum):
    """Enum representing the actions."""

    COPY = auto()
    INCREMENT = auto()
    DECREMENT = auto()
    JUMP = auto()


@dataclass
class Instruction:
    """Represents an instruction in the program."""

    action: Action
    first: str
    second: str


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
        self.program = []
        action_map = {
            "cpy": Action.COPY,
            "inc": Action.INCREMENT,
            "dec": Action.DECREMENT,
            "jnz": Action.JUMP,
        }
        pattern = compile(
            rf"(?P<action>({'|'.join(action_map.keys())})) "
            rf"(?P<first>(-?\d+|[abcd]))\s?"
            rf"(?P<second>(-?\d+|[abcd]))?"
        )
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.program.append(
                    Instruction(action_map[m["action"]], m["first"], m["second"])
                )
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._run()

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(c=1)

    def _run(self, **kwargs: int) -> int:
        # zero all registers
        reg = {k: 0 for k in "abcd"}

        # update registers with key word arguments
        reg |= kwargs

        # add all int literals as special registers
        for instruction in self.program:
            items = [instruction.first, instruction.second]
            for item in items:
                if item is not None and (
                    item.isdigit() or (item[0] == "-" and item[1:].isdigit())
                ):
                    reg[item] = int(item)

        i = 0
        while 0 <= i < len(self.program):
            if self.program[i].action == Action.COPY:
                reg[self.program[i].second] = reg[self.program[i].first]
            elif self.program[i].action == Action.INCREMENT:
                reg[self.program[i].first] += 1
            elif self.program[i].action == Action.DECREMENT:
                reg[self.program[i].first] -= 1
            elif (
                self.program[i].action == Action.JUMP
                and reg[self.program[i].first] != 0
            ):
                i += int(self.program[i].second) - 1
            i += 1

        return reg["a"]


if __name__ == "__main__":
    solver = Solver(load_puzzle_input_file(2016, 12))
    print(f"part one: {solver.solve_part_one()}")
    print(f"part two: {solver.solve_part_two()}")
