# Define custom function directory
ARG FUNCTION_DIR="/var/task/"

#
# Create the build image 
#
FROM --platform=linux/arm64 pypy:3.10-7.3.12-bookworm as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

# Update pip and setuptools
RUN pip install --upgrade pip setuptools

# Install awslambdaric
RUN pip install --target ${FUNCTION_DIR} awslambdaric

# Add the project files and install dependancies
COPY . ${FUNCTION_DIR}
RUN pip install --target ${FUNCTION_DIR} -r ${FUNCTION_DIR}/requirements.txt

#
# Create a slim runtime image from the build image
#
FROM --platform=linux/arm64 pypy:3.10-7.3.12-slim-bookworm

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set python to be pypy3
RUN ls -sf /opt/pypy/bin/pypy3 /usr/local/bin/python

# Set entry point and lambda handler
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["advent_of_code.app.lambda_handler"]




# # Define custom function directory
# ARG FUNCTION_DIR="/var/task/"

# #
# # Create the build image 
# #
# FROM --platform=linux/arm64 python:3.11.4-slim-bookworm as build-image

# # Include global arg in this stage of the build
# ARG FUNCTION_DIR
# RUN mkdir -p ${FUNCTION_DIR}

# # Update pip and setuptools
# RUN pip install --upgrade pip setuptools

# # Install aws-lambda-cpp build dependencies
# RUN apt-get update && \
#   apt-get install -y \
#   g++ \
#   make \
#   cmake \
#   unzip \
#   libcurl4-openssl-dev

# # Install awslambdaric
# RUN pip install --target ${FUNCTION_DIR} awslambdaric

# # Add the project files and install dependancies
# COPY . ${FUNCTION_DIR}
# RUN pip install --target ${FUNCTION_DIR} -r ${FUNCTION_DIR}/requirements.txt

# #
# # Create the runtime image from the build image
# #
# FROM --platform=linux/arm64 python:3.11.4-slim-bookworm

# # Include global arg in this stage of the build
# ARG FUNCTION_DIR
# # Set working directory to function root directory
# WORKDIR ${FUNCTION_DIR}

# # Copy in the built dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# # Set entry point and lambda handler
# ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# CMD ["advent_of_code.app.lambda_handler"]