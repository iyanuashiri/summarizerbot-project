FROM public.ecr.aws/lambda/python:3.8


RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY summaries.py ${LAMBDA_TASK_ROOT}


CMD ["summaries.lambda_handler"]
