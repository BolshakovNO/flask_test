# coding: utf-8
import urllib
from collections import Counter

from lxml import html

from . import celery, redis
import settings


@celery.task
def parse_url(url):
    print('Task started')
    # for i in range(0, 20):
    #     msg = 'Task message %s\n' % i
    #     redis.rpush(settings.MESSAGES_KEY, msg)
    #     redis.publish(settings.CHANNEL_NAME, msg)
    #     time.sleep(1)
    # redis.delete(settings.MESSAGES_KEY)
    page = urllib.urlopen(url)
    page_str = page.read()
    page.close()
    tags = html.fromstring(page_str)

    result = Counter([
        element.tag for element in tags.iter() if isinstance(element.tag, str)
    ])
    redis.publish('flask-socketio/parse', 'ok ok ok')
    # emit('parse complete', json.dumps(result.items()))
