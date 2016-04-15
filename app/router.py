# coding: utf-8
from flask import Flask, render_template

from . import app, socketio, settings
from .tasks import parse_url


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    print('Socket connected')


@socketio.on('task', namespace='/{}'.format(settings.CHANEL_NAME))
def make_task(data):
    parse_url.run(data['url'])
