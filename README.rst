========================
Djangae REST Autometrics
========================

This package installs models and middleware used to simplify user tracking across sessions and correlate access to resources to the user requesting such access.

Some of the tools in this project assume you are running in Google App Engine and using Django REST Framework for your views of interest. As such, the project depends on the `djangae` and `djangorestframework` packages. Some day perhaps I will split this into relational and non-relational sub-packages.


Quick start
-----------

1. Add "djangae_rest_autometrics" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangae_rest_autometrics',
    ]


TODO: finish setup steps

2. Include the djangae_rest_autometrics URLconf in your project urls.py like this::

    url(r'^metrics/', include('djangae_rest_autometrics.urls')),

3. Visit http://127.0.0.1:8000/metrics/ to view ?.