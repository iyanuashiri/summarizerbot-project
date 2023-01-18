FROM public.ecr.aws/lambda/python:3.8


RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY bot.py ${LAMBDA_TASK_ROOT}


CMD ["bot.lambda_handler"]
