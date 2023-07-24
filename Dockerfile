FROM public.ecr.aws/lambda/python:3.11

ARG wd=/var/task/

COPY . ${wd}
RUN chmod -R 0755 .
RUN pip install -r requirements.txt

CMD ["advent_of_code.app.lambda_handler"]

