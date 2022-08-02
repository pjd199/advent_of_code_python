"""Simple runner function for printing solver results with timings."""
from dataclasses import dataclass
from multiprocessing import Pool
from sys import stdout
from time import perf_counter_ns
from typing import Callable, Type, Union

from advent_of_code.utils.input_loader import load_puzzle_input_file
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class _Part:
    run: Callable[[], Union[int, str]]
    name: str


def _format_time(t: int) -> str:
    return f"{t / 1000000000:.2f}s"


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
        stdout.write(f"\rSolving {part.name}...")
        stdout.flush()
        with Pool(processes=1) as pool:
            start = perf_counter_ns()
            result = pool.apply_async(part.run)
            while not result.ready():
                stdout.write(
                    f"\rSolving {part.name} ({_format_time(perf_counter_ns() - start)})"
                )
                stdout.flush()
                result.wait(0.1)

            print(
                f"\rSolved {part.name}: {result.get()} "
                f"in {_format_time(perf_counter_ns() - start)}"
            )
