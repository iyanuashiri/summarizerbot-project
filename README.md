# summarizerbot-project


1. gunicorn 'summarizerbot:create_app()' --bind 0.0.0.0:5000

2. flask run
3. docker build -t summarizer-web .
4. docker run -d -p 5000:5000 summarizer-web
