# coding: utf-8
from celery import Celery
from flask import Flask


app = Flask(__name__)
app.config.from_object('settings')


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super(ContextTask, self).__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

from .views import url_parser

app.register_blueprint(url_parser)
