"""Unit test for advent_of_code.utils.sovler_interface."""

from advent_of_code.utils.solver_interface import SolverInterface


class _TestSolver(SolverInterface):
    YEAR = 123
    DAY = 456
    TITLE = "Test Title"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Noting to intialise.

        Args:
            puzzle_input (list[str]): ignored in testing
        """

    def solve_part_one(self) -> str:
        return "testing testing"

    def solve_part_two(self) -> int:
        return 123


def test_solver_interface() -> None:
    """Unit Test."""
    solver = _TestSolver([])
    assert solver.YEAR == 123
    assert solver.DAY == 456
    assert solver.TITLE == "Test Title"
    assert solver.solve_part_one() == "testing testing"
    assert solver.solve_part_two() == 123
