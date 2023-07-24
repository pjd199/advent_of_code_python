FROM public.ecr.aws/lambda/python:3.11

ARG wd=/var/task

COPY . ${wd}

RUN python -m pip install -r requirements.txt -t ${wd}

CMD ["advent_of_code.app.lambda_handler"]

