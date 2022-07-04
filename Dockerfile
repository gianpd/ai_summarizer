FROM public.ecr.aws/lambda/python:3.8

COPY requirements/prod.txt ${LAMBDA_TASK_ROOT}

RUN python3 -m ensurepip && python3 -m pip install --upgrade pip
RUN pip install -r prod.txt

ADD src ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]