import logging

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models

from djangae.fields import ListField

import settings


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

log = logging.getLogger(__name__)


class MetricsModel(models.Model):

    class Meta:
        app_label = 'autometrics_nonrel'
        abstract = True


class AccessManager(models.Manager):

    def filter(self, *args, **kwargs):
        if 'ids__contains' in kwargs:
            kwargs['ids__contains'] = str(kwargs['ids__contains'])
        return super(AccessManager, self).filter(*args, **kwargs)


class Access(MetricsModel):

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    session_key = models.CharField(max_length=40, null=True, editable=False)
    user = models.ForeignKey(USER_MODEL, null=True, editable=False)

    action = models.CharField(max_length=100, blank=False, editable=False)

    model = models.CharField(max_length=50, blank=False, editable=False)
    ids = ListField(models.CharField(max_length=100, editable=False))

    objects = AccessManager()


class UserSession(MetricsModel):

    session = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(USER_MODEL, null=True, editable=False)
    previous = models.ForeignKey('UserSession', null=True, editable=False)

    def save(self, set_ancestors_user=True, *args, **kwargs):
        super(UserSession, self).save(*args, **kwargs)
        if set_ancestors_user:
            self.set_ancestors_user(self.previous)

    def set_ancestors_user(self, parent):
        while (
                parent is not None
                and parent.user is None
                and parent.user != self.user
                ):
            parent.user = self.user
            parent.save(set_ancestors_user=False)
            parent = parent.previous


def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(
        user=user,
        session=request.session.session_key,
        )


user_logged_in.connect(user_logged_in_handler)
