"""A simple thread for displaying a message and a stopwatch."""
from threading import Event, Thread
from time import perf_counter_ns
from types import TracebackType


class DisplayTimer(Thread):
    """Thread to display the working time to the user."""

    def __init__(self, message: str, interval: float = 0.1) -> None:
        """Initialise the thread with the given message.

        Args:
            message (str): the message to display
            interval (float): the interval between printing updates
        """
        Thread.__init__(self, daemon=True)
        self.message = message
        self.interval = interval
        self.event = Event()

    def run(self) -> None:
        """Run the thread."""
        start = perf_counter_ns()
        while True:
            print(
                f"\r{self.message}"
                f"({(perf_counter_ns() - start) / 1000000000:.2f}s)",
                end="",
            )
            cancelled = self.event.wait(self.interval)
            if cancelled:
                break

    def __enter__(
        self,
    ) -> None:
        """Enter method called when entering a context."""
        self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit method called when leaving a context.

        Args:
            exc_type (type[BaseException] | None): optional exception
            exc_val (BaseException | None): optional exception value
            exc_tb (TracebackType | None): optional exception traceback
        """
        self.event.set()
        self.join()
