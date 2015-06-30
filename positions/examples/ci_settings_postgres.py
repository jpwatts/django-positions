from .settings_postgres import *

DATABASES['default'].update({'USER': 'postgres', 'PASSWORD': ''})
