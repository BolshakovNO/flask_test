# coding: utf-8
import os

from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from celery import Celery
from redis import StrictRedis

import settings
from tasks import parse_url


app = Flask(__name__)
app.config.from_object(settings)
app._static_folder = os.path.join(settings.BASE_DIR, 'static')
socketio = SocketIO(app, message_queue=settings.BROKER_URL)

redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

celery = Celery(
    __name__, backend=settings.BROKER_URL, broker=settings.BROKER_URL
)
celery.config_from_object(settings)
