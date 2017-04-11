import datetime
import mock

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test.client import Client

from ..functions import get_entity
from ..functions import get_entity_id_list
from ..functions import get_entity_list

from ..models import Access


class AccessEntityTest(TestCase):

    def setUp(self):
        self.entity = get_user_model().objects.create(username='entity')
        self.session = Client().session

    def _test_access_state(self, expected_user):
        time_before = datetime.datetime.now()
        get_entity(self.session, self.user, self.entity)
        time_after = datetime.datetime.now()
        self.assertEqual(Access.objects.count(), 1)
        access = Access.objects.get()
        self.assertTrue(time_before <= access.timestamp <= time_after)
        self.assertEqual(access.session_key, self.session.session_key)
        self.assertEqual(access.user, expected_user)
        self.assertEqual(access.action, 'get')
        self.assertEqual(access.model, self.entity._meta.db_table)
        self.assertEqual(len(access.ids), 1)
        self.assertEqual(access.ids[0], str(self.entity.pk))

    def test_access_entity(self):
        self.user = get_user_model().objects.create(username='user')
        self._test_access_state(self.user)

    def test_access_entity_no_user(self):
        self.user = None
        self._test_access_state(None)

    def test_access_entity_anon_user(self):
        self.user = AnonymousUser()
        self._test_access_state(None)


class ListEntityIdTest(TestCase):

    def setUp(self):
        self.entity_model = 'model'
        self.entity_ids = [123, 456, 789]
        self.session = Client().session

    def _test_list_state(self, expected_user):
        time_before = datetime.datetime.now()
        get_entity_id_list(
            self.session,
            self.user,
            self.entity_model,
            self.entity_ids,
            )
        time_after = datetime.datetime.now()
        self.assertEqual(Access.objects.count(), 1)
        access = Access.objects.get()
        self.assertTrue(time_before <= access.timestamp <= time_after)
        self.assertEqual(access.session_key, self.session.session_key)
        self.assertEqual(access.user, expected_user)
        self.assertEqual(access.action, 'list')
        self.assertEqual(access.model, self.entity_model)
        self.assertEqual(len(access.ids), 3)
        self.assertEqual(access.ids, [str(id) for id in self.entity_ids])

    def test_list_entities(self):
        self.user = get_user_model().objects.create(username='user')
        self._test_list_state(self.user)

    def test_list_entities_no_user(self):
        self.user = None
        self._test_list_state(None)

    def test_list_entities_anon_user(self):
        self.user = AnonymousUser()
        self._test_list_state(None)

    def test_list_no_entites_skips_save(self):
        get_entity_id_list(self.session, None, self.entity_model, [])
        self.assertEqual(Access.objects.count(), 0)


class ListEntityTest(TestCase):

    def setUp(self):
        import autometrics_nonrel.functions as f
        self.functions = f
        f.get_entity_id_list = mock.MagicMock(return_value='result')
        self.entities = [
            get_user_model().objects.create(username='e{0}'.format(i + 1))
            for i in range(3)
        ]
        self.session = 'session'
        self.user = 'user'
        self.entity_model = self.entities[0]._meta.db_table

    def test_entites_must_all_be_same_type(self):
        with self.assertRaises(AssertionError):
            get_entity_list(self.session, None, self.entities + [object()])

    def test_list_no_entites_skips_helper_method_call(self):
        get_entity_list(self.session, None, [])
        self.functions.get_entity_id_list.assert_not_called()

    def test_list_entities(self):
        result = get_entity_list(self.session, self.user, self.entities)
        self.assertEqual(result, 'result')
        self.functions.get_entity_id_list.assert_called_once()
        self.functions.get_entity_id_list.assert_called_with(
            self.session,
            self.user,
            self.entity_model,
            [e.pk for e in self.entities],
        )
