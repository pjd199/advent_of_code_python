"""Simple runner function for printing solver results with timings."""
from typing import Type

from advent_of_code.utils.display_timer import DisplayTimer
from advent_of_code.utils.function_timer import function_timer
from advent_of_code.utils.input_loader import load_puzzle_input_file
from advent_of_code.utils.solver_interface import SolverInterface


def runner(solver_class: Type[SolverInterface]) -> None:
    """Run the Solver, printing results with timings.

    Args:
        solver_class (Type[SolverInterface]): The solver to run
    """
    print(f"Solving '{solver_class.TITLE}' [{solver_class.YEAR}-{solver_class.DAY:02}]")
    solver = solver_class(load_puzzle_input_file(solver_class.YEAR, solver_class.DAY))

    with DisplayTimer("Solving part one: "):
        result, time = function_timer(solver.solve_part_one)
    print(f"\rSolved part one: {result} " f"in {time / 1000:.2f}s")

    if solver_class.DAY != 25:
        with DisplayTimer("Solving part two: "):
            result, time = function_timer(solver.solve_part_two)
        print(f"\rSolved part two: {result} " f"in {time / 1000:.2f}s")
