from google.appengine.ext import vendor
vendor.add('sitepackages')

import os  # noqa
from django.core.wsgi import get_wsgi_application  # noqa
from djangae.wsgi import DjangaeApplication  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = DjangaeApplication(get_wsgi_application())
