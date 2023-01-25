#!/bin/sh


#flask db upgrade

#flask run --host 0.0.0.0:5000

exec gunicorn 'summarizerbot:create_app()' --bind 0.0.0.0:5000



