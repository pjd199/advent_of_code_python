"""A simple thread for displaying a message and a stopwatch."""
from sys import stdout
from threading import Event, Thread
from time import perf_counter_ns

NANO_IN_SEC = 1000000000


class DisplayTimer(Thread):
    """Thread to display the working time to the user."""

    def __init__(self, message: str):
        """Initialise the thread with the given message.

        Args:
            message (str): the message to display
        """
        Thread.__init__(self, daemon=True)
        self.message = message
        self.event = Event()

    def run(self) -> None:
        """Run the thread."""
        start = perf_counter_ns()
        while not self.event.wait(0.1):
            stdout.write(
                f"\r{self.message}"
                f"({(perf_counter_ns() - start) / NANO_IN_SEC:.2f}s)"
            )
            stdout.flush()

    def cancel(self) -> None:
        """Cancel the timer."""
        self.event.set()
        self.join()
