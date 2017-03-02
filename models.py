import datetime
import logging

from django.contrib.auth.models import AnonymousUser
from django.db import models

from accounts.models import User


log = logging.getLogger(__name__)


class RawActionManager(models.Manager):

    def record(self, session_key, user, action):
        if isinstance(user, AnonymousUser):
            user = None
        return RawAction.objects.create(
            timestamp=datetime.datetime.now(),
            session_key=session_key,
            user=user if user else None,
            action=action,
        )


class RawAction(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    session_key = models.CharField(max_length=100, editable=False)
    user = models.ForeignKey(User, null=True, editable=False)

    action = models.CharField(max_length=100, editable=False)

    objects = RawActionManager()
