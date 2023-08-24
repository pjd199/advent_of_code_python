# Advent of Code Solver RESTful API

[![python versions](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)](https://www.python.org/)
![os platforms](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-blue)
![cloud platform](https://img.shields.io/badge/cloud-AWS%20Lambda-blue)

[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/pjd199/advent_of_code_python/CI-CD-pipeline.yaml?branch=main?label=CI%2FCD%20pipeline)](https://github.com/pjd199/advent_of_code_python/actions/workflows/CI-CD-pipeline.yaml)
[![codecov](https://codecov.io/gh/pjd199/advent_of_code_python/branch/main/graph/badge.svg?token=CZGMDWH4SH)](https://codecov.io/gh/pjd199/advent_of_code_python)
[![Website](https://img.shields.io/website?down_message=offline&label=RESTful%20API&up_message=ok&url=https%3A%2F%2Fjnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws%2F)](https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws)

[![GitHub](https://img.shields.io/github/license/pjd199/advent_of_code_python?color=black)](./license.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

[Advent of Code](https://adventofcode.com/) is an annual coding challenge by
[Eric Wastl](http://was.tl/). Some take up the challenge for the glory of the
hall of fame. Others, like me, use the daily puzzles as a way of learning a new
language. And so, this project is the story of my journey into
[Python](https://www.python.org/) - the language, the ecosystem and the whole
Pythnoic world. Blended with years of experience as a Software Engineer, the aim
is to compose solutions that are elegant, robust and fully tested. Oh, and
deployed as a RESTful API using [Flask](https://palletsprojects.com/p/flask/),
[AWS Lambda](https://aws.amazon.com/lambda/), with
[Github Actions](https://github.com/features/actions) providing for a CI/CD
pipleline with automated test, build and deploy functionality. Free to try it
out below, just don't spoil your fun by using the API until you've solved the
puzzle by yourself!!!

## Progress on Development Branch

![status](https://raw.githubusercontent.com/pjd199/advent_of_code_python/dev/status.gif)

## Built with

- [Python](https://www.python.org/)
- [Flask](https://palletsprojects.com/p/flask/)
- [AWS Serverless Application Model](https://aws.amazon.com/serverless/sam/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Github Actions](https://github.com/features/actions)
- [Github Codespaces](https://github.com/features/codespaces)

## Installation and Deployment

### Prerequisites

- [Python 3.10-3.11](https://www.python.org/)
- [AWS SAM CLI and AWS Credentials](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [AWS Credentials](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html) -
  locally or as secrets for Github Action

### Installation in a prodcution environment

```sh
pip install advent_of_code_solver@git+https://github.com/pjd199/advent_of_code_python
```

### Installation in a development environment:

```sh
git clone https://github.com/pjd199/advent_of_code_python
pip install --editable .[dev]
```

### Deployment

Deployment requires [AWS Lambda](https://aws.amazon.com/lambda) and
[Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3), both of
which included in the [AWS Free Tier](https://aws.amazon.com/free). Usage
outside the free tier may be charged.

1. Build the app with SAM

```
sam build
```

2. Deploy to AWS, using the --guided option on the first call to set stack names
   and locations, which will be saved in samconfig.toml

```
sam deploy --guided
```

If you encounter problems during deployment, the
[AWS SAM Hello World](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)
tutorial has a good troubleshooting section.

### Clean up

If AWS stack is no longer required, run:

```
sam delete
```

## Usage

### Using the RESTful API

An deployment of the RESTful API for this project is available at
[https://api.adventofcode.dibdin.me/](https://api.adventofcode.dibdin.me/). If
installed and deployed by another user, use the URL provided at the end of the
SAM deploy process.

#### Resource Endpoints

The resource endpoints for this API are:

- / - the root resource, listing of all resources available on this API
- /calendars - the calendar resource, listing valid puzzle years and days
- /puzzles - the puzzles resouce, detailing of all the puzzles
- /answers - the answers resource, to find the answer to a specific puzzle
- /system - the system resource, providing information about the API system

The body of the response is in JSON format, with the HTTP header containing one
of the following standard status codes:

- 200 - success
- 404 - no solver for requested date or path does not exist
- 500 - server error, including errors in the puzzle input file

#### /

The root resource, listing of all resources available on this API

```sh
curl http://api.adventofcode.dibdin.me
```

```JSON
{
  "api_version": "2.0.0",
  "description": "Discover resourses available through this API.",
  "links": [
    {
      "action": "GET",
      "description": "Discover available puzzles and answers, filtered using /calendars/{year}.",
      "href": "api.adventofcode.dibdin.me/calendars",
      "rel": "calendars"
    },
    {
      "action": "GET",
      "description": "Discover detailed puzzle information, filtered using /puzzles/{year}/{day}.",
      "href": "api.adventofcode.dibdin.me/puzzles",
      "rel": "puzzles"
    },
    {
      "action": "GET",
      "description": "Find answer for given input by calling /answers/{year}/{day} with puzzle input as POST body or URL provided as input paramerater.",
      "href": "api.adventofcode.dibdin.me/answers",
      "parameters": ["input"],
      "rel": "answers"
    },
    {
      "action": "POST",
      "description": "Find answer for given input by calling /answers/{year}/{day} with puzzle input as POST body or URL provided as input paramerater.",
      "href": "api.adventofcode.dibdin.me/answers",
      "rel": "answers"
    }
  ],
  "results": ["calendars", "puzzles", "answers"],
  "self": "http://api.adventofcode.dibdin.me",
  "timestamp": "2023-07-31T11:23:33Z"
}
```

#### /calendars

The calendars resource, listing valid puzzle years and days. Filtered using
/calendars/{year} (for example /calendar/2015).

```sh
curl https://api.adventofcode.dibdin.me/calendars
```

```JSON
{
  "api_version": "2.0.0",
  "description": "List of available puzzles, filtered using /calendars/{year}",
  "links": [],
  "results": [
    {
      "days": [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
        19, 20, 21, 22, 23, 24, 25
      ],
      "links": [
        {
          "action": "GET",
          "description": "Discover detailed puzzle information for 2015.",
          "href": "http://api.adventofcode.dibdin.me/puzzles/2015",
          "rel": "puzzles"
        }
      ],
      "year": 2015
    },
    {
      "days": [1, 2],
      "links": [
        {
          "action": "GET",
          "description": "Discover detailed puzzle information for 2016.",
          "href": "http://api.adventofcode.dibdin.me/puzzles/2016",
          "rel": "puzzles"
        }
      ],
      "year": 2016
    }
  ],
  "self": "http://api.adventofcode.dibdin.me/calendars",
  "timestamp": "2016-12-02T16:23:41Z"
}
```

#### /puzzles

The puzzles resource, listing detailed puzzle information. Filtered using
/puzzles/{year} or /puzzles/{year}/{day} (eg /puzzles/2022 or /puzzles/2022/25)

```sh
curl https://api.adventofcode.dibdin.me/puzzles/2015/1
```

```JSON
{
  "timestamp": "2023-08-03T16:56:21Z",
  "self": "http://api.adventofcode.dibdin.me/puzzles/2015/1",
  "api_version": "2.0.0",
  "description": "Detailed puzzle information, filtered using /puzzles/{year}/{day}",
  "results": [
    {
      "year": 2015,
      "day": 1,
      "title": "Not Quite Lisp",
      "excerpt": "Santa was hoping for a white Christmas, but his weather machine's \"snow\" function is powered by stars, and he's fresh out!  To save Christmas, he needs you to collect fifty stars by December 25th.",
      "has_part_one": true,
      "has_part_two": true,
      "part_one_solved": true,
      "part_two_solved": true,
      "completion_date": "2022-07-09T19:08:56+01:00",
      "timings": {
        "unit": "ms",
        "parse": 6,
        "part_one": 0,
        "part_two": 0
      },
      "official_url": "https://adventofcode.com/2015/day/1",
      "repository_url": "https://github.com/pjd199/advent_of_code_python/blob/main/advent_of_code/year2015/day1.py",
      "code_url": "https://raw.githubusercontent.com/pjd199/advent_of_code_python/main/advent_of_code/year2015/day1.py",
      "links": [
        {
          "rel": "answers",
          "href": "http://api.adventofcode.dibdin.me/answers/2015/1",
          "description": "Get the answer for 2015 day 1.",
          "action": "GET",
          "parameters": ["input"]
        },
        {
          "rel": "answers",
          "href": "http://api.adventofcode.dibdin.me/answers/2015/1",
          "description": "Get the answer for 2015 day 1.",
          "action": "POST"
        }
      ]
    }
  ],
  "links": []
}
```

#### /answers/{year}/{day}

Solve the puzzle for the requested year and day. There are two options for
providing the puzzle input.

1. The URL of a puzzle input file can be passed in using the input query
   parameter when requesting with the HTTP GET method.

```sh
curl https://api.adventofcode.dibdin.me/answers/2015/2?input=https://raw.githubusercontent.com/pjd199/advent_of_code_python/main/puzzle_input/year2015/day2.txt
```

2. The puzzle input file can be uploaded using the HTTP POST method.

```sh
curl -X POST -H "Content-Type: text/plain" -d "@day2.txt"  https://api.adventofcode.dibdin.me/answers/2015/2

```

```JSON
{
  "timestamp": "2023-07-31T10:32:54Z",
  "self": "http://localhost:5000/answers/2015/2",
  "api_version": "{version}",
  "description": "Get the answer to the puzzle, with input file provide as POST, or URL provided as input paramerater.",
  "results": {
    "year": 2015,
    "day": 2,
    "part_one": "1598415",
    "part_two": "3812909",
    "timings": {
      "units": "ms",
      "parse": 5,
      "part_one": 0,
      "part_two": 0
    }
  },
  "links": [
    {
      "rel": "puzzles",
      "href": "http://api.adventofcode.dibdin.me/puzzles/2015/2",
      "description": "Get the puzzle information for 2015 day 2.",
      "action": "GET"
    }
  ]
}
```

#### /system

The system resource, displaying useful system information.

```JSON
{
    "timestamp": "2023-08-24T13:18:34Z",
    "self": "https://api.adventofcode.dibdin.me/system",
    "api_version": "2.0.0",
    "description": "System information.",
    "results": {
        "url": "https://api.adventofcode.dibdin.me/system",
        "host": "api.adventofcode.dibdin.me",
        "platform": "Linux-4.14.255-311-248.529.amzn2.aarch64-aarch64-with-glibc2.36",
        "machine": "aarch64",
        "architecture": "64bit",
        "compiler": "CPython 3.11.4",
        "license_url": "https://raw.githubusercontent.com/pjd199/advent_of_code_python/main/license.md",
        "license": "MIT"
    },
    "links": []
}
```

### Daily Helper utility

This project includes a helper script for downloading the puzzle and input
puzzle file from the Advent of Code website. It also creates a template Solver
file for the puzzle, and updates the unit test.

To reduce requests to the Advent of Code website, a cache is created in the root
of the project folder.

```
$ daily_helper 2015 1
```

For all the optional parameters, run

```
$ daily_helper --help
```

#### Session Cookie

A session cookie is required to download answers and part two. To locate and
store the session cookie:

1. Open a web browser (Chrome, Edge or Mozilla)
2. Log into the Advent of Code website
3. Right click on the page, and select inspect
4. On the application tab, select cookies
5. Copy the value of the session cookie
6. Store the session cookie using the following command

```
daily_helper --save_session <<<PASTE VALUE HERE>>
```

### Testing

This project has unit tests, integration tests and system tests (which can only
be run after the deployment phase).

```sh
pytest /tests/unit
pytest /tests/integration
pytest /tests/system
```

## Roadmap

- [ ] Test against multiple sets of puzzle input files
- [ ] Wait for Advent of Code to start on 1st December 2023!!!

## Licence

Distributed under the MIT License. See [licence.md](./license.md) for more
information.

## Author

Pete Dibdin
