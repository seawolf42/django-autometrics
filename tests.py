import uuid

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import RawAction


class RawActionTest(TestCase):
	
	def setUp(self):
		self.user = get_user_model().objects.create(username='abc')
		self.action = RawAction.objects.create()
	
	def test_fields(self):
		self.assertIsNone(self.action.user)
	
	def test_properties(self):
		self.assertIsNone(self.action.user_id)
	
	def test_set_user(self):
		self.action.user = self.user
		self.action.save()
		self.assertEquals(self.action.user_id, self.user.id)
