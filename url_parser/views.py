# coding: utf-8
from flask import Blueprint, render_template

from . import celery, app

url_parser = Blueprint(
    'url_parser', __name__,
    template_folder=app.config['TEMPLATES_FOLDER']
)


@url_parser.route('/')
def show():
    return render_template('index.html')


@url_parser.route('/parse', methods=['POST'])
def parse_handler(*args, **kwargs):

    return 'success'


@celery.task()
def parse_url(url):
    pass
