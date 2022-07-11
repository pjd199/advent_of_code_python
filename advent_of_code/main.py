"""Command line interface for Advent of Code Solver."""
from datetime import date
from importlib import import_module
from pathlib import Path
from sys import argv, exit, path
from time import perf_counter_ns


def _main() -> None:
    """Solve the specified day and print the results."""
    from advent_of_code.utils.input_loader import load_file
    from advent_of_code.utils.solver_status import implementation_status

    print("*************************")
    print("* Advent of Code Solver *")
    print("*************************")

    solvers = implementation_status()

    if len(argv) == 3 and argv[1].isnumeric() and argv[2].isnumeric():
        year = int(argv[1])
        day = int(argv[2])
        if date(year, 12, day) not in solvers:
            print(f"Invalid date for AoC: year={year}, day={day}")
            exit(1)
        if not solvers[date(year, 12, day)]:
            print(f"Solver not implemented: year={year}, day={day}")
            exit(2)
    else:
        while True:
            year = int(input("Year: "))
            day = int(input("Day: "))
            if date(year, 12, day) not in solvers:
                print(f"Invalid date for AoC: year={year}, day={day}")
            elif not solvers[date(year, 12, day)]:
                print(f"Solver not implemented: year={year}, day={day}")
            else:
                break
    print()
    print(f"Solving AoC year {year}, day {day}")

    # load the input file
    puzzle_input = load_file(f"./puzzle_input/year{year}/day{day}.txt")

    # dynamically instantiate the class
    mod = import_module(f"advent_of_code.year{year}.day{day}")
    solver = mod.Solver(puzzle_input)

    # time the execution of the solver
    start_time = perf_counter_ns()
    answers = solver.solve_all()
    end_time = perf_counter_ns()
    elapsed_time = end_time - start_time

    for i, ans in enumerate(answers):
        print(f"Part {i+1}: {ans}")

    if elapsed_time <= 1000000:
        print("Time: <1ms")
    elif elapsed_time >= 1000000000:
        print(f"Time: {elapsed_time / 1000000000:.2f}s")
    else:
        print(f"Time: {(elapsed_time) // 1000000}ms")


if __name__ == "__main__":
    path.append(str(Path(__file__).parent.parent))
    _main()
