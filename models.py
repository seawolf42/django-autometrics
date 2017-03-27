import logging

from django.db import models

from accounts.models import User


log = logging.getLogger(__name__)


class Access(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    session_key = models.CharField(max_length=100, editable=False)
    user = models.ForeignKey(User, null=True, editable=False)

    action = models.CharField(max_length=100, editable=False)

    resource = models.CharField(max_length=500, editable=False)

    class Meta:
        app_label = 'metrics'
