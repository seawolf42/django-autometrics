import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test.client import Client

from ..functions import access_entity
from ..functions import list_entities

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
        self.assertEqual(access.model, self.entity._meta.db_table)
        self.assertEqual(len(access.ids), 1)
        self.assertEqual(access.ids[0], self.entity.pk)

    def test_access_entity(self):
        self.user = get_user_model().objects.create(username='user')
        self._test_access_state(self.user)

    def test_access_entity_no_user(self):
        self.user = None
        self._test_access_state(None)

    def test_access_entity_anon_user(self):
        self.user = AnonymousUser()
        self._test_access_state(None)


class ListEntityTest(TestCase):

    def setUp(self):
        self.entities = [
            get_user_model().objects.create(username='e{0}'.format(i + 1))
            for i in range(3)
        ]
        self.session = Client().session

    def _test_list_state(self, expected_user):
        time_before = datetime.datetime.now()
        list_entities(self.session, self.user, self.entities)
        time_after = datetime.datetime.now()
        self.assertEqual(Access.objects.count(), 1)
        access = Access.objects.get()
        self.assertTrue(time_before <= access.timestamp <= time_after)
        self.assertEqual(access.session_key, self.session.session_key)
        self.assertEqual(access.user, expected_user)
        self.assertEqual(access.action, 'list')
        self.assertEqual(access.model, self.entities[0]._meta.db_table)
        self.assertEqual(len(access.ids), 3)
        self.assertEqual(access.ids, [e.pk for e in self.entities])

    def test_list_entities(self):
        self.user = get_user_model().objects.create(username='user')
        self._test_list_state(self.user)

    def test_list_entities_no_user(self):
        self.user = None
        self._test_list_state(None)

    def test_list_entities_anon_user(self):
        self.user = AnonymousUser()
        self._test_list_state(None)
