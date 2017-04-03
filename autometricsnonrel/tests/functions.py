import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test.client import Client

from ..functions import access_entity

from ..models import Access


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
        self.assertEqual(len(access.resources), 1)
        self.assertEqual(access.resources[0], '{0}:{1}'.format(
            self.entity._meta.db_table,
            self.entity.pk,
            ))

    def test_access_entity(self):
        self.user = get_user_model().objects.create(username='user')
        self._test_access_state(self.user)

    def test_access_entity_no_user(self):
        self.user = None
        self._test_access_state(None)

    def test_access_entity_anon_user(self):
        self.user = AnonymousUser()
        self._test_access_state(None)
