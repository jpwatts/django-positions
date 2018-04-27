from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_positions',
        'USER': 'django_positions',
        'PASSWORD': 'django_positions',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
