# Define custom function directory
ARG FUNCTION_DIR="/var/task/"

#
# Create the build image 
#
FROM --platform=linux/arm64 python:3.11.4-slim-bookworm as build-image

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

# Install awslambdaric
RUN pip install --target ${FUNCTION_DIR} awslambdaric

# add the project files
WORKDIR ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}
#RUN chmod -R 0755 ${FUNCTION_DIR}
RUN pip install --target ${FUNCTION_DIR} -r requirements.txt

#
# Create the runtime image from the build image
#
FROM --platform=arm64 python:3.11.4-slim-bookworm

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set entry point and lambda
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

# set the AWS Lambda handler
CMD ["advent_of_code.app.lambda_handler"]