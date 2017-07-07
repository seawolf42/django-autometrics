from djangae.settings_base import *  # noqa

import logging
import sys


if sys.argv[1] == 'test':
    logging.disable(logging.CRITICAL)


SECRET_KEY = 'gh30b@s+meh9fusgy_&wt=m-wxu!-e75icg-=0y2ywle4@0ees'

# Activate django-dbindexer for the default database
DATABASES = {
    'default': {
        'ENGINE': 'djangae.db.backends.appengine'
    }
}

INSTALLED_APPS = (
    'djangae',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
