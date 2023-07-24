FROM public.ecr.aws/lambda/python:3.11

ARG wd=/var/task

COPY . ${LAMBDA_TASK_ROOT}

RUN python3.11 -m pip install -r requirements.txt -t ${LAMBDA_TASK_ROOT}

CMD ["advent_of_code.app.lambda_handler"]

