from djangae.settings_base import *  # noqa

import logging
import sys


if sys.argv[1] == 'test':
    logging.disable(logging.CRITICAL)


SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz'

DATABASES = {
    'default': {
        'ENGINE': 'djangae.db.backends.appengine'
    }
}

AUTH_USER_MODEL = 'gauth_datastore.GaeDatastoreUser'

INSTALLED_APPS = (
    'djangae',

    'django.contrib.auth',
    'djangae.contrib.gauth_datastore',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',

    'djangae.contrib.contenttypes',
    'djangae.contrib.security',

    'autometrics_nonrel',
)

MIDDLEWARE_CLASSES = (
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
    'session_csrf.CsrfMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'autometrics_nonrel.middleware.UserSessionTrackingMiddleware',
    'djangae.contrib.gauth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'djangae.contrib.gauth_datastore.backends.AppEngineUserAPIBackend',
)
