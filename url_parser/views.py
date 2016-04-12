# coding: utf-8
from flask import Blueprint, render_template

from settings import TEMPLATES_FOLDER

url_parser = Blueprint(
    'url_parser', __name__, template_folder=TEMPLATES_FOLDER)


@url_parser.route('/')
def show():
    return render_template('index.html')


@url_parser.route('/parse', methods=['POST'])
def parse(*args, **kwargs):
    return 'success'
