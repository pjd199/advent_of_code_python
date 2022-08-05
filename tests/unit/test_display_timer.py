"""Unit test for advent_of_code.utils.display_timer."""
from re import compile
from time import sleep

import pytest

from advent_of_code.utils.display_timer import DisplayTimer


@pytest.mark.parametrize(
    ("interval", "duration"), [(0.1, 2), (0.2, 3), (0.5, 4), (1.0, 5)]
)
def test_display_timer(
    capfd: pytest.CaptureFixture[str], interval: float, duration: int
) -> None:
    """Unit test for the DisplayTimer class.

    Args:
        capfd: the stdout / stderr capture fixture
        interval(float): the parametrized interval
        duration(int): the number of seconds to run the timer for
    """
    # execute display timer
    message = "TEST "
    dt = DisplayTimer(message, interval)
    dt.start()
    sleep(duration)
    dt.cancel()
    captured = capfd.readouterr().out

    # check capture is as expected
    pattern = compile(r"(\r.*\(\d+.\d\ds\))*")
    assert pattern.fullmatch(captured)

    # check each line in the capture for ascending time in
    # increaments, with a tolerance of 1s
    line_pattern = compile(rf"\r{message}\((?P<time>\d+.\d\d)s\)")
    total_time = 0.0
    for m in line_pattern.finditer(captured):
        assert m is not None
        time = float(m["time"])
        assert (time == 0.0) or (time > total_time)
        assert time < (total_time + interval + 1.0)
        total_time = time
