import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.test.client import Client

from ..functions import access_entity

from ..models import Access


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

    def test_fields(self):
        self.assertEquals(self.access.user, self.user)
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


class AccessEntityTest(TestCase):

    def setUp(self):
        self.entity = get_user_model().objects.create(username='entity')
        self.session = Client().session

    def _test_access_state(self, expected_user):
        time_before = datetime.datetime.now()
        access_entity(self.session, self.user, self.entity)
        time_after = datetime.datetime.now()
        self.assertEqual(Access.objects.count(), 1)
        access = Access.objects.get()
        self.assertTrue(time_before <= access.timestamp <= time_after)
        self.assertEqual(access.session_key, self.session.session_key)
        self.assertEqual(access.user, expected_user)
        self.assertEqual(access.action, 'access')
        self.assertEqual(access.resource, '{0}:{1}'.format(self.entity._meta.db_table, self.entity.pk))

    def test_access_entity(self):
        self.user = get_user_model().objects.create(username='user')
        self._test_access_state(self.user)

    def test_access_entity_no_user(self):
        self.user = None
        self._test_access_state(None)

    def test_access_entity_anon_user(self):
        self.user = AnonymousUser()
        self._test_access_state(None)
