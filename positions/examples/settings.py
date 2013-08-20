SECRET_KEY = 'sekr3t'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'positions.examples.lists',
    'positions.examples.nodes',
    'positions.examples.generic',
    'positions.examples.todo',
    'positions.examples.store',
    'positions.examples.photos',
    'positions.examples.school',
    'positions.examples.restaurants',
)
