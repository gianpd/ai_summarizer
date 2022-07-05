FROM public.ecr.aws/lambda/python:3.8

COPY requirements/prod.txt ${LAMBDA_TASK_ROOT}

RUN python3 -m ensurepip && python3 -m pip install --upgrade pip
RUN pip install -r prod.txt

ADD ./src/ ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]

#TODO: https://docs.aws.amazon.com/lambda/latest/dg/images-create.html

# # Define function directory
# ARG FUNCTION_DIR="/function"

# FROM python:3.8.13-slim-buster as build-image

# # Install aws-lambda-cpp build dependencies
# RUN apt-get update && \
#   apt-get install -y \
#   g++ \
#   make \
#   cmake \
#   unzip \
#   libcurl4-openssl-dev

# # Include global arg in this stage of the build
# ARG FUNCTION_DIR
# # Create function directory
# RUN mkdir -p ${FUNCTION_DIR}

# # ADD function code
# ADD ./src/ ${FUNCTION_DIR}

# # Install the runtime interface client
# RUN pip install \
#         --target ${FUNCTION_DIR} \
#         awslambdaric

# # Multi-stage build: grab a fresh copy of the base image
# FROM python:3.8.13-slim-buster

# # Include global arg in this stage of the build
# ARG FUNCTION_DIR
# # Set working directory to function root directory
# WORKDIR ${FUNCTION_DIR}

# # Copy in the build image dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# # install dependencies
# COPY requirements/prod.txt ${FUNCTION_DIR}
# RUN python -m pip install --upgrade pip\
#   && pip install --target ${FUNCTION_DIR} -r prod.txt

# ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# CMD [ "main.handler" ]