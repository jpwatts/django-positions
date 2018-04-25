from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_positions',
        'USER': 'django_positions',
        'PASSWORD': 'django_positions',
    }
}

LOGGING['handlers']['debug_log_file']['formatter'] = 'simple'
