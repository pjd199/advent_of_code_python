FROM --platform=linux/arm64 public.ecr.aws/lambda/python:3.11

COPY . /var/task/
RUN chmod -R 0755 .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["advent_of_code.app.lambda_handler"]

