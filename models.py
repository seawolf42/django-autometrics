import datetime
import logging

from django.db import models
from djangae.fields import ListField

from accounts.models import User


log = logging.getLogger(__name__)


class RawAction(models.Model):
	
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	
	session_key = models.CharField(max_length=100, editable=False)
	user = models.ForeignKey(User, null=True, editable=False)
	
	action = models.CharField(max_length=100, editable=False)
