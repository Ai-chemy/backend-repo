from .base import *

ALLOWED_HOSTS = ["localhost", "192.168.50.6"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DATABASE_NAME"),
        'USER': config("DATABASE_USER"),
        'PASSWORD': config("DATABASE_USER_PASSWORD"),
        'HOST': config("DATABASE_HOST"),
        'PORT': config("DATABASE_PORT"),
    }
}