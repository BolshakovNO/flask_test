# coding: utf-8
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

BROKER_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)

CHANEL_NAME = 'parse'

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "asdqeqwewqedsafdagrwgrbfx"

# Secret key for signing cookies
SECRET_KEY = "asdasdadvdsvfdabxgdqdsedsafcd"

# DB

