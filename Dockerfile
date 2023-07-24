FROM public.ecr.aws/lambda/python:3.9

ARG wd=/var/task

COPY . ${LAMBDA_TASK_ROOT}

RUN python3.11 -m pip install -r requirements.txt

CMD ["advent_of_code.app.lambda_handler"]

