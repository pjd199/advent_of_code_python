"""Unit tests for the lambda_handler function."""
from json import load

import pytest

from advent_of_code.lambda_handler import lambda_handler

with open("./tests/test_lambda_handler.json") as file:
    data = load(file)


@pytest.mark.parametrize(("event"), range(len(data["event"])))
def test_lambda_handler(event: int) -> None:
    """Run test cases against lambda_handler().

    Args:
        event (int): the event number in the JSON
    """
    # test the data has matching event and response numbers
    assert event < len(data["response"]), (
        f"Response for event " f"{event} does not exist"
    )

    # test each event gives the expected response
    assert (
        lambda_handler(data["event"][event], None) == data["response"][event]
    ), f"Error on event {event}"
