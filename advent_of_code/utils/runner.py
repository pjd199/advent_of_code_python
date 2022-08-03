"""Simple runner function for printing solver results with timings."""
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Callable, Type, Union

from advent_of_code.utils.display_timer import NANO_IN_SEC, DisplayTimer
from advent_of_code.utils.input_loader import load_puzzle_input_file
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class _Part:
    run: Callable[[], Union[int, str]]
    name: str


def runner(solver_class: Type[SolverInterface]) -> None:
    """Run the Solver, printing results with timings.

    Args:
        solver_class (Type[SolverInterface]): The solver to run
    """
    print(f"Solving '{solver_class.TITLE}' [{solver_class.YEAR}-{solver_class.DAY:02}]")
    solver = solver_class(load_puzzle_input_file(solver_class.YEAR, solver_class.DAY))
    parts = [_Part(solver.solve_part_one, "part one")]
    if solver_class.DAY != 25:
        parts += [_Part(solver.solve_part_two, "part two")]

    for part in parts:
        # start the display timer
        display_timer = DisplayTimer(f"Solving {part.name}: ")
        display_timer.start()

        # time the solver
        start = perf_counter_ns()
        result = part.run()
        stop = perf_counter_ns()

        # stop the display timer
        display_timer.cancel()

        # print the results
        print(
            f"\rSolved {part.name}: {result} " f"in {(stop - start) / NANO_IN_SEC:.2f}s"
        )
