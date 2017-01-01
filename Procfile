web: uwsgi --master --die-on-term --module app:app --http :31337 --gevent 40 --gevent-monkey-patch
dev: FLASK_APP=app.py FLASK_DEBUG=1 flask run -h 0.0.0.0 -p 31337
