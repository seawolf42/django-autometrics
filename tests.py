import uuid

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import RawAction


class RawActionTest(TestCase):
	
	def setUp(self):
		self.action = RawAction.objects.create()
	
	def test_fields(self):
		pass
	
	def test_properties(self):
		pass
