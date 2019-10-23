import os

db = os.environ['DB']
v = tuple(map(int, os.environ['DJANGO_VERSION'].strip().split('.')))


_DB_ENGINES = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_positions',
        'USER': 'root',
        'PASSWORD': '',
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_positions',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

if v > (2, 0, 0):
    from .base_settings_2 import *
else:
    from .base_settings import *

if db in DATABASES:
    DATABASES['default'] = _DB_ENGINES[db]
