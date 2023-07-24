# Define custom function directory
ARG FUNCTION_DIR="/var/task/"

FROM --platform=linux/arm64 python:3.11-slim as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Install the function's dependencies
RUN pip install --target ${FUNCTION_DIR} awslambdaric

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

COPY . ${FUNCTION_DIR}
RUN chmod -R 0755 .
RUN pip install -r requirements.txt

CMD ["advent_of_code.app.lambda_handler"]