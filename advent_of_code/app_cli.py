"""Run the Flask app from the commandline."""
from json import JSONDecodeError, dumps
from os import environ
from pathlib import Path
from sys import path
from threading import Thread
from time import sleep

from requests import get

if __name__ == "__main__":
    path.append(str(Path(__file__).parent.parent))  # pragma: no cover

from advent_of_code import app
from advent_of_code.utils.function_timer import function_timer


def app_cli() -> None:  # pragma: no cover
    """Run the command line interface."""
    # start the development server on the localhost
    scheme = "https"
    host = "127.0.0.1"
    port = 5000
    environ["FLASK_ENV"] = "development"
    print(f"Starting {scheme} server on {host} at {port}")
    flask_thread = Thread(
        target=lambda: app.app.run(
            host=host,
            port=port,
            use_reloader=False,
            ssl_context="adhoc" if scheme == "https" else None,
        )
    )
    flask_thread.daemon = True
    flask_thread.start()

    # allow the server time to start
    sleep(1)

    # print basic instructions
    print("---")
    print("Type 'exit' to shutdown server and exit")
    print("---")
    print("Available routes:")
    print(" - /")
    print(" - /calendars/{year}")
    print(" - /puzzles/{year}")
    print(" - /puzzles/{year}/{day}")
    print(" - /answers/{year}/{day}?input={url_for_puzzle_input_file}")
    print(" - /system")
    print(" - /license")
    print("eg - /answers/2015/25")
    print("---")

    # loop until Ctrl-C exits the loop
    while True:
        print()
        url = input("Enter route path: ")
        if url in ["exit", "quit", "exit()"]:
            break

        try:
            print(f"Requesting {scheme}://{host}:{port}{url}")
            # time the call to the development server
            response, elapsed_time = function_timer(
                get, f"{scheme}://{host}:{port}{url}", timeout=300, verify=False
            )

            # print the headers
            print("Response Headers")
            print("================")
            print(dumps(dict(response.headers)))
            print()

            # pretty print the results
            print("Response Body")
            print("=============")
            print(dumps(response.json(), indent=4))
            print()

            # print the elapsed time
            print("Time")
            print("====")
            if elapsed_time == 0:
                print("Round Trip Time: <1ms")
            elif elapsed_time >= 1000:
                print(f"Round Trip Time: {elapsed_time / 1000:.2f}s")
            else:
                print(f"Round Trip Time: {elapsed_time}ms")

        except JSONDecodeError as e:
            print(e)


if __name__ == "__main__":
    # run if file executed from the command line
    app_cli()  # pragma: no cover
