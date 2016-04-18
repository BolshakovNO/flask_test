# coding: utf-8
from threading import Thread, Event
import os
import urllib
from datetime import datetime
from collections import Counter

from flask import (
    Flask, render_template, request, copy_current_request_context, jsonify
)
from flask.ext.socketio import SocketIO, emit
from celery import Celery
from lxml import html
import rethinkdb
from rethinkdb.errors import RqlRuntimeError

from . import settings


app = Flask(__name__)
app.config.from_object(settings)
app._static_folder = os.path.join(settings.BASE_DIR, 'static')
socketio = SocketIO(app, message_queue=settings.BROKER_URL)

celery = Celery(
    app.import_name, backend=settings.BROKER_URL, broker=settings.BROKER_URL
)
celery.config_from_object(settings)


def db_setup():
    connection = rethinkdb.connect()
    try:
        rethinkdb.db_create(settings.DB_NAME).run(connection)
        (
            rethinkdb.db(settings.DB_NAME)
            .table_create(settings.COMPLETED_TABLE).run(connection)
        )
        print 'Database setup completed'
    except RqlRuntimeError:
        print 'Database already exists.'
    finally:
        connection.close()
db_setup()

connection = rethinkdb.connect()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_task', methods=['POST'])
def make_task():
    url = request.form['url']

    data = (
        rethinkdb.db(settings.DB_NAME)
        .table(settings.COMPLETED_TABLE)
        .filter({'url': url})
        .run(connection)
    )
    if data.items:
        return jsonify({'result': {
            'data': data.items[0].get('result'), 'url': url
        }})

    try:
        page = urllib.urlopen(url)
        page_str = page.read()
        page.close()
        task = parse_url.delay(page_str, url)
    except IOError:
        return jsonify({'error': 'Cannot open url: {}'.format(url)})
    except BaseException as err:
        return jsonify({'error': 'Complete with error: {}'.format(str(err))})

    return jsonify({'task_id': task.id})


@celery.task(bind=True)
def parse_url(self, page_str, url):
    print('Task started')
    tags = html.fromstring(page_str)

    result = Counter([
        element.tag for element in tags.iter() if isinstance(element.tag, str)
    ])
    print(result)
    print('Task completed')
    rethinkdb.db(settings.DB_NAME).table(settings.COMPLETED_TABLE).insert({
        'result': result.items(),
        'date': str(datetime.now()),
        'url': url,
        'task_id': self.request.id
    }).run(connection)


@socketio.on('connect')
def connect():
    print('Socket connected')


@socketio.on('monitor')
def connect(task_id):
    task = parse_url.AsyncResult(task_id)
    thread = Thread()
    thread_stop_event = Event()

    class MonitorThread(Thread):
        def __init__(self):
            super(MonitorThread, self).__init__()

        @copy_current_request_context
        def monitor(self):
            while not thread_stop_event.isSet():
                if task.state == 'SUCCESS':
                    data = (
                        rethinkdb.db(settings.DB_NAME)
                        .table(settings.COMPLETED_TABLE)
                        .filter({'task_id': task.id})
                        .run(connection)
                    )
                    emit('parse_complete', {
                        'data': data.items[0].get('result'),
                        'url': data.items[0].get('url')
                    })
                    break

        def run(self):
            self.monitor()

    if not thread.isAlive():
        print("Starting Thread")
        thread = MonitorThread()
        thread.start()



