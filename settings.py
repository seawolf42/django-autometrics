from djangae.settings_base import *  # noqa


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

    'rest_framework',
    'rest_framework.authtoken',

    'autometricsnonrel',
)

MIDDLEWARE_CLASSES = (
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'autometricsnonrel.middleware.UserSessionTrackingMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}
