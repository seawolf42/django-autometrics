==========================
Django Autometrics Non-Rel
==========================

This package installs models and middleware used to simplify user tracking across sessions and correlate access to resources to the user requesting such access.

Some of the tools in this project assume you are running in a non-relational environment (so far only Google App Engine is supported) for your views of interest. As such, the project depends on the `djangae` package. Some day perhaps I will split this into relational and non-relational sub-packages.


Quick start
-----------

1. Add "autometricsnonrel" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'autometricsnonrel',
    ]


TODO: finish setup steps

2. Include the djangae_rest_autometrics URLconf in your project urls.py like this::

    url(r'^metrics/', include('autometricsnonrel.urls')),

3. Visit http://127.0.0.1:8000/metrics/ to view ?.
