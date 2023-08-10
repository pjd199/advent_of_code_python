"""Function for timing functions."""
from time import perf_counter_ns
from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def function_timer(
    function: Callable[P, T], *args: P.args, **kwargs: P.kwargs
) -> tuple[T, int]:
    """Function for timing functions, called with args and kwargs.

    Args:
        function (Callable[P, T]): the function to call
        *args (P.args): arguments passed to function
        **kwargs (P.kwargs): keyword arguments passed to function

    Returns:
        tuple[T, int]: the result, plus the time in milliseconds
    """
    start_time = perf_counter_ns()
    result = function(*args, **kwargs)
    stop_time = perf_counter_ns()
    return result, (stop_time - start_time) // 1000000
