# coding: utf-8
import os

from celery import Celery
from flask import Flask, send_from_directory


app = Flask(__name__, static_url_path='/static')
app.config.from_object('settings')
app._static_folder = app.config['STATIC_FOLDER']


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
