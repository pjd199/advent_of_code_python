# Advent of Code Solver RESTful API

[![python versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/)
![platforms](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-blue)

[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pjd199/advent_of_code_python/CI-CD-Pipeline/main?label=CI%2FCD%20Pipeline)](https://github.com/pjd199/advent_of_code_python/actions/workflows/CI-CD-pipeline.yaml)
[![codecov](https://codecov.io/gh/pjd199/advent_of_code_python/branch/main/graph/badge.svg?token=CZGMDWH4SH)](https://codecov.io/gh/pjd199/advent_of_code_python)
[![Website](https://img.shields.io/website?down_message=offline&label=AWS%20Lambda&up_message=ok&url=https%3A%2F%2Fjnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws%2F)](https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

[Advent of Code](https://adventofcode.com/) is an annual coding challenge by
[Eric Wastl](http://was.tl/). Some take up the challenge for the glory of the
hall of fame. Others, like me, use the daily puzzles as a way of learning a
new language. And so, this project is the story of my journey into
[Python](https://www.python.org/) - the language, the ecosystem and the whole
Pythnoic world. Blended with years of experience as a Software Engineer,
the aim is to compose solutions that are elegant, robust and fully tested.
Oh, and deployed as a RESTful API using
[Flask](https://palletsprojects.com/p/flask/),
[AWS Lambda](https://aws.amazon.com/lambda/),
with [Github Actions](https://github.com/features/actions) providing for a 
CI/CD pipleline with automated test, build and deploy functionality. 
Free to try it out below, just don't spoil your fun by using the API until 
you've solved the puzzle by yourself!!!

## Built with

* [Python](https://www.python.org/)
* [Flask](https://palletsprojects.com/p/flask/)
* [AWS Serverless Application Model](https://aws.amazon.com/serverless/sam/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [Github Actions](https://github.com/features/actions)

## Installation and Deployment

### Prerequisites

* [Python 3.8-3.11](https://www.python.org/)
* [AWS SAM CLI and AWS Credentials](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

### Installation

1. Clone the repo

``` sh
git clone https://github.com/pjd199/advent_of_code_python
```

2. Install dependancies

In a prodcution environment:

```sh
pip install -r requirements.txt
```

In a test and development environment:

```sh
pip install -r requirements_dev.txt
```

### Deployment

1. Build the app with SAM

```
sam build
```

2. Deploy to AWS, using the --guided option on the first call to set 
   stack names and locations, which will be saved in samconfig.toml

```
sam deploy --guided
```

*If you encounter problems during deployment, the 
[AWS SAM Hello World](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html) tutorial has a good troubleshooting section.*

### Clean up

If AWS stack is no longer required, run: 

```
sam delete
```

## Usage

### Using the RESTful API

An deployment of the RESTful API for this project is available at 
[https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws](https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws). 
If installed and deployed by another user, use the URL provided at the end of the 
SAM deploy process.

#### Endpoints

The endpoints for this API are listed below. The body of the response is in 
JSON format, with the HTTP header containing one of the following standard 
status codes:

* 200 - success
* 404 - no solver for requested date or path does not exist
* 500 - server error, including errors in puzzle input file The
 

#### /

A list of puzzle solutions, listed by year and day

``` sh
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws
```

``` JSON
{"years":[{"days":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],"year":2015},{"days":[1],"year":2016}]}
```

#### /{year}

A list of puzzles which have been solved for the requested year.

``` sh
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015
```

``` JSON
{"days":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],"year":2015}
```

#### /{year}/{day}

Solve the puzzle for the requested year and day. There are three options
for providing the puzzle input.

1. The URL of a puzzle input file can be passed in using the input query
   parameter when requesting with the HTTP GET method.
2. The puzzle input file can be uploaded using the HTTP POST method.
3. If no puzzle input is provided, the author's puzzle input is used by
   default.

``` sh
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1?input=https://raw.githubusercontent.com/pjd199/advent_of_code_python/main/puzzle_input/year2015/day1.txt
```

``` sh
curl -X POST -H "Content-Type: text/plain" -d "@day1.txt"  https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1/part_one

```

``` sh
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1
```

``` JSON
{"day":1,"part_one":"74","part_two":"1795","year":2015}
```

#### /{year}/{day}/part_one

As above, but only solves part one of the puzzle.

``` sh
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1/part_one
```

``` JSON
{"day":1,"part_one":"74","year":2015}
```

#### /{year}{day}/part_two

As above, but only solves part two of the puzzle.

``` sh
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1/part_two
```

``` JSON
{"day":1,"part_two":"1795","year":2015}
```

### Command Line Interface

Run the Advent of Code Solver form the command line, entering the year and date
when prompted.

``` sh
python .\advent_of_code\main.py
```

``` sh
*************************
* Advent of Code Solver *
*************************
Year: 2015
Day: 1

Solving AoC year 2015, day 1
Part 1: 74
Part 2: 1795
Time: 1ms
```

Alternatively, the year and the date may be provided as arguments on the
command line:

``` sh
python .\advent_of_code\main.py 2015 1
```

### Testing

This project has unit tests, integration tests and system tests (which can only
be run after the deployment phase).

``` sh
pytest
```

## Roadmap

* [ ] Add puzzle metadata, including title and description
* [ ] Test against multiple sets of puzzle input files
* [X] Solve puzzles for 2015
* [ ] Solve puzzles for 2016
* [ ] Solve puzzles for 2017
* [ ] Solve puzzles for 2018
* [ ] Solve puzzles for 2019
* [ ] Solve puzzles for 2020
* [ ] Solve puzzles for 2021
* [ ] Wait for the release of the next Adevent of Code adventure on
  1st December 2022.

## Licence

Distributed under the MIT License. See [licence.md](./license.md)
for more information.

## Author

Pete Dibdin

## Acknowledgements

* The updated Flask AWS Lambda interface is forked from [CodeSchwert](https://github.com/CodeSchwert/flask-aws-lambda)
* There are many helpful Python tutorials on [Real Python](https://realpython.com/)
* The
  [AWS SAM Hello World](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)
  tutorial is a great introduction to working with AWS Lambda
