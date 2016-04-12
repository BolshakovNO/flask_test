# coding: utf-8
from flask import Flask

from settings import (
    make_celery, CELERY_BROKER_URL, CELERY_RESULT_BACKEND,
)
from url_parser.views import url_parser

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL=CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND
)
celery = make_celery(app)

app.register_blueprint(url_parser)

if __name__ == '__main__':
    app.run()
