# pull official base image
FROM python:3.8.10-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
# Prevents Python from writing pyc files to disc
# Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./requirements/dev.txt ./

RUN pip install --upgrade pip \
    && pip install -r dev.txt

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5010", "--reload"]
