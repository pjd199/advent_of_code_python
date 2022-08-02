"""A helper script for downloading puzzle webpages and puzzle input."""
from argparse import ArgumentParser
from json import dump, load
from pathlib import Path
from re import match
from typing import Any, Dict, List, Optional, Union

import pytest
from bs4 import BeautifulSoup
from markdownify import ATX, markdownify  # type: ignore
from requests import get

AOC_ROOT = "https://adventofcode.com"
CACHE_PATH = ".aoc_website_cache"


class DailyHelper:
    """The help for a specific day."""

    def __init__(
        self,
        year: int,
        day: int,
        session: Optional[str] = None,
        flush: bool = False,
        verbose: bool = False,
        test: bool = False,
    ):
        """Initialise the helper for a specific day.

        Args:
            year (int): the year for the puzzle
            day (int): the day for the puzzle
            session (Optional[str]): the session cookie for the Advent of Code website
            flush (bool): if True, ignores cached files. Default False
            verbose (bool): if True, enables logging. Default False
            test (bool): if True, enables testing. Default False
        """
        self.year = year
        self.day = day
        self.session = session
        self.flush = flush
        self.verbose = verbose
        self.test = test

        self.title = ""
        self.answers: List[str] = []

        self.html_path = Path(f"{CACHE_PATH}/year{year}/day{day}/index.html")
        self.part_one_path = Path(f"{CACHE_PATH}/year{year}/day{day}/part_one.md")
        self.part_two_path = Path(f"{CACHE_PATH}/year{year}/day{day}/part_two.md")
        self.response_path = Path(f"{CACHE_PATH}/year{year}/day{day}/response.json")
        self.unit_test_data_path = Path("tests/unit/test_dayX.json")
        self.puzzle_input_path = Path(f"puzzle_input/year{year}/day{day}.txt")
        self.template_python_path = Path(f"advent_of_code/year{year}/day{day}.py")
        self.template_text_path = Path("advent_of_code/daily_helper_template.txt")

    def run(self) -> None:
        """The download, parsing and file creation sequence."""
        self._flush()

        # download the webpage from Advent of Code website
        self._download(
            f"{AOC_ROOT}/{self.year}/day/{self.day}",
            self.html_path,
        )

        # parse the html file
        with open(self.html_path) as file:
            soup = BeautifulSoup(file, "html.parser")

        # find and save the part descriptions
        parts = soup.find_all("article", attrs={"class": "day-desc"})
        md_paths = [self.part_one_path, self.part_two_path]
        for i in range(min(len(parts), len(md_paths))):
            self._save(
                md_paths[i], markdownify(str(parts[i]), heading_style=ATX, wrap=80)
            )

        # save the puzzle input file
        self._download(
            f"{AOC_ROOT}/{self.year}/day/{self.day}/input", self.puzzle_input_path
        )

        # find the puzzle title
        h2 = soup.find_all("h2")
        for x in h2:
            if m := match(r"--- Day (?:[\d]+): (?P<title>[\w|\s]+) ---", x.string):
                self.title = m["title"]

        # find and save the answers, if solved
        para = soup.find_all("p")
        for x in para:
            if str(x.contents[0]).startswith("Your puzzle answer was"):
                self.answers.append(x.code.string)
        self._save_response()

        # save the answers in the unit test data
        self._save_unit_test_data()

        # create and save a new python solver file
        desc = soup.find_all("article", attrs={"class": "day-desc"})
        for d in desc:
            d.h2.extract()

        with open(self.template_text_path) as file:
            template = "".join(file.readlines())

        self._save(
            self.template_python_path,
            template.format(
                year=self.year,
                day=self.day,
                title=self.title.replace('"', "'"),
                part_one=self._markdown_pydoc(str(desc[0])),
                part_two=(
                    "<<<INSERT PART TWO HERE>>>"
                    if len(desc) == 1
                    else self._markdown_pydoc(desc[1])
                ),
            ),
            ok_if_exists=True,
        )

        # run the testing
        self._testing()

    def _log(self, data: Any) -> None:
        if self.verbose:
            print(str(data))

    def _flush(self) -> None:
        if self.flush:
            self._log("Flushing cache...")
            paths_to_remove = [
                self.html_path,
                self.part_one_path,
                self.part_two_path,
                self.response_path,
                self.puzzle_input_path,
            ]
            for path in paths_to_remove:
                self._log(f"Removing {path}")
                path.unlink(missing_ok=True)

    def _save(
        self,
        path: Path,
        data: Union[str, Dict[str, Any]],
        force: bool = False,
        ok_if_exists: bool = False,
    ) -> None:
        if not force and path.is_file():
            if ok_if_exists:
                self._log(f"{path} already exists")
            else:
                self._log(f"{path} already exists - use --flush to overwrite")
        else:
            with open(path, "w") as file:
                if isinstance(data, str):
                    file.write(data)
                else:
                    dump(data, file, indent=4)
                self._log(f"Saved {path}")

    def _save_unit_test_data(self) -> None:
        answers = self.answers

        # update the unit test data if required
        with open(self.unit_test_data_path) as file:
            unit_test_data = load(file)
        changes = False
        if str(self.year) not in unit_test_data:
            unit_test_data[str(self.year)] = {}
            changes = True

        if not self.flush and str(self.day) in unit_test_data[str(self.year)]:
            if unit_test_data[str(self.year)][str(self.day)] != self.answers:
                self._log(f"!!! conflict in {self.unit_test_data_path} !!!")
                self._log(f"Found {unit_test_data[str(self.year)][str(self.day)]}")
                self._log(f"Expected {answers}")
            else:
                self._log(f"Answers already stored in {self.unit_test_data_path}")
        else:
            if len(answers) == 2:
                unit_test_data[str(self.year)][str(self.day)] = answers
            elif len(answers) == 1:
                unit_test_data[str(self.year)][str(self.day)] = [answers[0], ""]
            else:
                unit_test_data[str(self.year)][str(self.day)] = ["", ""]
            changes = True

        if changes:
            # sort unit_test_data by numeric strings
            # ie ["1","2","10"] not ["1", "10", "2"]
            def sorted_dict(d: Dict[str, Any]) -> Dict[str, Any]:
                return dict(sorted(d.items(), key=lambda x: int(x[0])))

            sorted_data = sorted_dict(
                {k: sorted_dict(v) for k, v in unit_test_data.items()}
            )

            self._save(self.unit_test_data_path, sorted_data, force=True)

    def _save_response(self) -> None:
        response = {
            "title": self.title,
            "year": self.year,
            "day": self.day,
        }
        if len(self.answers) > 0:
            response["part_one"] = self.answers[0]

        if len(self.answers) > 1:
            response["part_two"] = self.answers[1]

        # save the answers
        self._save(Path(self.response_path), response)

    def _download(self, url: str, path: Path) -> None:
        if path.is_file():
            self._log(f"{path} already exists - use --flush to overwrite")
        else:
            self._log(f"Downloading {url}")
            path.parent.mkdir(parents=True, exist_ok=True)
            if self.session:
                response = get(url, headers={"cookie": f"session={self.session}"})
            else:
                response = get(url)
            if response.status_code == 200:
                self._save(path, response.text)
                self._log(f"Saved {path}")
            else:
                raise RuntimeError(
                    f"Unable to download file: "
                    f"server status code {response.status_code}"
                )

    def _markdown_pydoc(self, text: str) -> str:
        return (
            str(markdownify(str(text), heading_style=ATX, wrap=True, wrap_width=72))
            .replace("\t", "    ")
            .replace("\n\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
            .replace('"', "'")
            .strip()
        )

    def _testing(self) -> None:
        # test the solver if requested
        if self.test:
            options = [
                "./tests/unit",
                "-k",
                f"{self.year}-{self.day:02}",
                f"--cov=advent_of_code.year{self.year}.day{self.day}",
                "--no-cov-on-fail",
                "--cov-fail-under=100",
            ]
            if self.verbose:
                options += ["-v", "--cov-report", "term-missing"]
            else:
                options += ["-q", "--cov-report="]
            pytest.main(options)


def main() -> None:
    """Main function, called from the command line."""
    parser = ArgumentParser(
        description="Helper for downloading puzzles and input from"
        "the Advent of Code website."
    )
    parser.add_argument("year", type=int, help="the year to download.")
    parser.add_argument(
        "day",
        type=int,
        help="the day to download.",
    )
    parser.add_argument(
        "--session",
        "-s",
        type=str,
        help="set the session cookie for the Advent of Code website.",
        action="store",
    )
    parser.add_argument(
        "--save_session",
        "-ss",
        help="set and store the session cookie for the Advent of Code website",
        action="store",
        metavar="SESSION",
    )
    parser.add_argument(
        "--flush",
        "-f",
        help="flush the cache for this year and day",
        action="store_true",
    )
    parser.add_argument("--verbose", "-v", help="verbose mode", action="store_true")
    parser.add_argument("--test", "-t", help="run unit tests", action="store_true")
    args = parser.parse_args()

    # handle the session cookie loading and saving
    session_path = Path(f"{CACHE_PATH}/.session")
    if args.session:
        session = args.session
    elif args.save_session:
        session = args.save_session
        with open(session_path, "w") as file:
            file.write(session)
    elif session_path.is_file():
        with open(session_path) as file:
            session = file.readline()
    else:
        session = None

    helper = DailyHelper(
        args.year, args.day, session, args.flush, args.verbose, args.test
    )
    helper.run()


if __name__ == "__main__":
    main()
