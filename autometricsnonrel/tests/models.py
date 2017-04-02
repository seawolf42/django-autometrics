import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test.client import Client

from ..models import Access
from ..models import UserSession


class AccessTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(AccessTest, cls).setUpClass()
        cls.user = get_user_model().objects.create(username='user')

    def setUp(self):
        self.time_before = datetime.datetime.now()
        self.access = Access.objects.create(
            session_key='12345',
            user=self.user,
            action='action',
            resource='resource'
            )
        self.time_after = datetime.datetime.now()

    def test_default_fields(self):
        self.assertEqual(self.access.user, self.user)
        self.assertIsNotNone(self.access.session_key)
        self.assertGreater(self.access.timestamp, self.time_before)
        self.assertLess(self.access.timestamp, self.time_after)
        self.assertIsNotNone(self.access.action)
        self.assertIsNotNone(self.access.resource)

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


class UserSessionTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user')
        self.session = Client().session
        self.session_key = self.session.session_key
        self.user_session = UserSession.objects.create(
            session=self.session_key,
            )

    def test_default_fields(self):
        self.assertEqual(self.user_session.session, self.session_key)
        self.assertIsNone(self.user_session.user)
        self.assertIsNone(self.user_session.previous)

    def test_foreign_key_relationship(self):
        session_2 = Client().session
        UserSession.objects.create(
            session=session_2.session_key,
            user=self.user,
            previous=self.user_session,
        )
        self.assertEqual(UserSession.objects.count(), 2)
        self.assertEqual(
            UserSession.objects.get(previous=self.session_key).previous,
            self.user_session,
            )
