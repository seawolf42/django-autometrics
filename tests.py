import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import RawAction


class RawActionTest(TestCase):
	
	@classmethod
	def setUpClass(cls):
		super(RawActionTest, cls).setUpClass()
		cls.user = get_user_model().objects.create(username='abc')
	
	def setUp(self):
		self.time_before = datetime.datetime.now()
		self.action = RawAction.objects.create(
			session_key='12345',
			user=self.user,
			action='blah',
			)
		self.time_after = datetime.datetime.now()
	
	def test_fields(self):
		self.assertEquals(self.action.user, self.user)
		self.assertIsNotNone(self.action.session_key)
		self.assertGreater(self.action.timestamp, self.time_before)
		self.assertLess(self.action.timestamp, self.time_after)
		self.assertIsNotNone(self.action.action)
	
	def test_properties(self):
		self.assertEquals(self.action.user_id, self.user.id)
	
	def test_session_key_is_not_nullable(self):
		self.action.session_key = None
		with self.assertRaises(IntegrityError):
			self.action.save()
	
	def test_user_is_nullable(self):
		self.action.user = None
		self.action.save()
	
	def test_action_is_not_nullable(self):
		self.action.action = None
		with self.assertRaises(IntegrityError):
			self.action.save()
