FROM public.ecr.aws/lambda/python:3.8

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY nltk_data ${LAMBDA_TASK_ROOT}
COPY summarize.py ${LAMBDA_TASK_ROOT}

CMD ["summarize.lambda_handler"]
