import logging

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models

import settings


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

log = logging.getLogger(__name__)


class MetricsModel(models.Model):

    class Meta:
        app_label = 'autometricsnonrel'
        abstract = True


class Access(MetricsModel):

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    session_key = models.CharField(max_length=40, editable=False)
    user = models.ForeignKey(USER_MODEL, null=True, editable=False)

    action = models.CharField(max_length=100, editable=False)

    resource = models.CharField(max_length=500, editable=False)


class UserSession(MetricsModel):

    session = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(USER_MODEL, null=True)
    previous = models.ForeignKey('UserSession', null=True)


def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(
        user=user,
        session=request.session.session_key,
        )


user_logged_in.connect(user_logged_in_handler)
