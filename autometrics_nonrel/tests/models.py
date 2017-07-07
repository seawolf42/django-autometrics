import datetime

import mock

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test.client import Client

from ..models import Access
from ..models import UserSession


class AccessManagerTest(TestCase):

    def setUp(self):
        self.id = 123
        Access.objects.create(
            session_key='12345',
            user=None,
            action='action',
            model='model',
            ids=[self.id],
            )
        self.access = Access.objects.get()

    def test_filter_converts_ids_to_strings(self):
        id = self.id
        self.assertEqual(Access.objects.filter(ids__contains=id).count(), 1)
        self.assertEqual(
            Access.objects.filter(ids__contains=str(self.id)).count(),
            1,
            )


class AccessTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user')
        self.time_before = datetime.datetime.now()
        self.access = Access.objects.create(
            session_key='12345',
            user=self.user,
            action='action',
            model='model',
            )
        self.time_after = datetime.datetime.now()

    def test_default_fields(self):
        self.assertEqual(self.access.user, self.user)
        self.assertIsNotNone(self.access.session_key)
        self.assertGreater(self.access.timestamp, self.time_before)
        self.assertLess(self.access.timestamp, self.time_after)
        self.assertIsNotNone(self.access.action)
        self.assertIsNotNone(self.access.model)
        self.assertEqual(len(self.access.ids), 0)

    def test_properties(self):
        self.assertEquals(self.access.user_id, self.user.id)

    def test_ids_are_strings(self):
        id = 123
        self.access.ids = [id]
        self.access.save()
        access = Access.objects.get()
        self.assertEqual(access.ids[0], str(id))

    def test_session_key_is_nullable(self):
        self.access.session_key = None
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
        self.assertIsNotNone(self.user_session.created)
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

    def test_save_sets_ancestors(self):
        self.user_session.set_ancestors_user = mock.MagicMock()
        self.user_session.save()
        self.user_session.set_ancestors_user.assert_called_once()

    def test_save_skips_set_ancestors_if_param_unset(self):
        self.user_session.set_ancestors_user = mock.MagicMock()
        self.user_session.save(set_ancestors_user=False)
        self.user_session.set_ancestors_user.assert_not_called()

    def test_set_ancestors_walks_up_parent_list(self):
        next_session = self.user_session
        for i in range(3):
            next_session = UserSession.objects.create(
                session=Client().session.session_key,
                previous=next_session,
            )
        last_session = next_session
        self.assertEqual(UserSession.objects.filter(user=None).count(), 4)
        last_session.user = self.user
        last_session.save()
        self.assertEqual(UserSession.objects.filter(user=None).count(), 0)

    def test_set_ancestors_stops_if_parent_user_is_not_none(self):
        next_session = self.user_session
        for i in range(3):
            next_session = UserSession.objects.create(
                session=Client().session.session_key,
                previous=next_session,
            )
        self.user_session.user = get_user_model().objects.create(
            username='user2',
            )
        self.user_session.save(set_ancestors_user=False)
        last_session = next_session
        self.assertEqual(UserSession.objects.filter(user=None).count(), 3)
        last_session.user = self.user
        last_session.save()
        self.assertEqual(UserSession.objects.filter(user=self.user).count(), 3)
