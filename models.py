import datetime
import logging

from django.db import models
from djangae.fields import ListField

from accounts.models import User


log = logging.getLogger(__name__)


class RawAction(models.Model):
	pass
