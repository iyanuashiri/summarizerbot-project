FROM python:3.9-bullseye

WORKDIR /summarizer_web

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#COPY app app
#COPY migrations migrations
#COPY tests tests
#COPY summarizerbot.py .flaskenv entrypoint.sh __init__.py ./
#COPY __init__.py /summarizer_web/
COPY . /summarizer_web/

ENV FLASK_APP="summarizerbot.py"

RUN chmod +x /summarizer_web/entrypoint.sh
#RUN chmod +x entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]

#CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]





