# Advent of Code Serverless API

[![python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/) ![platforms](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-blue)

[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pjd199/advent_of_code_python/CI-CD-Pipeline/main?label=CI%2FCD%20Pipeline)](https://github.com/pjd199/advent_of_code_python/actions/workflows/CI-CD-pipeline.yaml) [![codecov](https://codecov.io/gh/pjd199/advent_of_code_python/branch/main/graph/badge.svg?token=CZGMDWH4SH)](https://codecov.io/gh/pjd199/advent_of_code_python) ![Website](https://img.shields.io/website?down_message=offline&label=AWS%20Lambda&up_message=ok&url=https%3A%2F%2Fjnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws%2F)

## About
[Advent of Code](https://adventofcode.com/) is an annual coding challenge by [Eric Wastl](http://was.tl/). Some take up the challenge for the glory of the hall of fame. Others, like me, use the daily puzzles as a way of learning a new language. And so, this project is the story of my journey into [Python](https://www.python.org/) - the language, the ecosystem and the whole Pythnoic world. Blended with years of experience as a Software Engineer, the aim is to compose solutions that are elegant, robust and fully tested. Oh, and deployed as a RESTful API using [Flask](https://palletsprojects.com/p/flask/), [AWS Lambda](https://aws.amazon.com/lambda/), and * [Github Actions](https://github.com/features/actions) for a CI/CD pipleline with automated test, build and deplay functionality. Free to try it out below, just don't spoil your fun by using the API until you've solved the puzzle by yourself!!!

## Built with

* [Python](https://www.python.org/)
* [Flask](https://palletsprojects.com/p/flask/)
* [AWS Serverless Application Model](https://aws.amazon.com/serverless/sam/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [Github Actions](https://github.com/features/actions)

## Getting Started

## RESTful API
The RESTful API for this project is available at https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/. The API supports the following endpoints and successful responses are returned in JSON with a status code of 200.

### /
A list of puzzle solutions, listed by year and day
```
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws

{"years":[{"days":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],"year":2015},{"days":[1],"year":2016}]}
```

### /{year}
A list of puzzles which have been solved for the requested year.
```
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015

{"days":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],"year":2015}
```

### /{year}/{day}
Solve the puzzle for the requested year and day. There are three options for providing the puzzle input.
* The URL of a puzzle input file can be passed in using the input query parameter when requested using the GET method.
* The puzzle input file can be uploaded using the POST method.
* If not puzzle input is provided, the solver uses the author's puzzle input.

```
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1?input=https://raw.githubusercontent.com/pjd199/advent_of_code_python/main/puzzle_input/year2015/day1.txt
```
```
curl -X POST -H "Content-Type: text/plain" -d "@day1.txt"  https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1/part_one

```
```
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1
```
```JSON
{"day":1,"part_one":"74","part_two":"1795","year":2015}
```

### /{year}/{day}/part_one
As above, but only solves part one of the puzzle.
```
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1/part_one
```
```JSON
{"day":1,"part_one":"74","year":2015}
```

### /{year}{day}/part_two
As above, but only solves part two of the puzzle.
```
curl https://jnrxshzkvnbexzeedxptq54ugq0mqlpe.lambda-url.eu-west-2.on.aws/2015/1/part_two
```
```JSON
{"day":1,"part_two":"1795","year":2015}
```
## Installation and Deployment

### Prerequisites

### Installation

### Deployment to AWS Lambda

## Usage

### Command Line Interface

## Roadmap

## Licence
![GitHub](https://img.shields.io/github/license/pjd199/advent_of_code_python?color=blue)
Distributed under the MIT License. See [licence.md](license.md) for more information.

## Author
Pete Dibdin

## Acknowledgements