import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import Access


class AccessTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(AccessTest, cls).setUpClass()
        cls.user = get_user_model().objects.create(username='abc')

    def setUp(self):
        self.time_before = datetime.datetime.now()
        self.access = Access.objects.create(
            session_key='12345',
            user=self.user,
            action='blah',
            )
        self.time_after = datetime.datetime.now()

    def test_fields(self):
        self.assertEquals(self.access.user, self.user)
        self.assertIsNotNone(self.access.session_key)
        self.assertGreater(self.access.timestamp, self.time_before)
        self.assertLess(self.access.timestamp, self.time_after)
        self.assertIsNotNone(self.access.action)

    def test_properties(self):
        self.assertEquals(self.access.user_id, self.user.id)

    def test_session_key_is_not_nullable(self):
        self.access.session_key = None
        with self.assertRaises(IntegrityError):
            self.access.save()

    def test_user_is_nullable(self):
        self.access.user = None
        self.access.save()

    def test_action_is_not_nullable(self):
        self.access.action = None
        with self.assertRaises(IntegrityError):
            self.access.save()
