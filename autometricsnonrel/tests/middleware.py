from django.test import TestCase

import logging
import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.signals import user_logged_in
from django.test import RequestFactory
from django.test.client import Client

from ..middleware import UserSessionTrackingMiddleware
from ..models import UserSession


log = logging.getLogger()


class MockRequest():
    pass


class UserSessionTrackingMiddlewareBaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(UserSessionTrackingMiddlewareBaseTest, cls).setUpClass()
        cls.middleware = UserSessionTrackingMiddleware()
        cls.user = get_user_model().objects.create(username='user')

    def setUp(self):
        self.request = MockRequest()
        self.request.user = self.user
        self.session = Client().session
        self.session_key = self.session.session_key


class UserSessionTrackingRequestTest(UserSessionTrackingMiddlewareBaseTest):

    def test_request_with_no_session_sets_pmetrics_key_none(self):
        self.assertFalse(hasattr(self.request, 'session'))
        self.middleware.process_request(self.request)
        self.assertIsNone(self.request.pmetrics_key)

    def test_request_with_session_sets_pmetrics_key_to_session_key(self):
        self.request.session = self.session
        self.middleware.process_request(self.request)
        self.assertEqual(self.request.pmetrics_key, self.session_key)


class UserSessionTrackingResponseTest(UserSessionTrackingMiddlewareBaseTest):

    def setUp(self):
        super(UserSessionTrackingResponseTest, self).setUp()
        self.request.session = self.session
        self.request.session.cycle_key = mock.MagicMock(return_value=None)
        self.request.pmetrics_key = self.session_key

    def test_response_with_user_none_passes(self):
        del self.request.user
        self.middleware.process_response(self.request, None)

    def test_response_with_anonymous_user_passes(self):
        self.request.user = AnonymousUser()
        self.middleware.process_response(self.request, None)

    def test_response_with_anonymous_user_and_changed_session_passes(self):
        self.request.user = AnonymousUser()
        self.request.pmetrics_key = 'abc'
        self.middleware.process_response(self.request, None)

    def test_response_with_no_request_session_key_cycles_key(self):
        self.request.session = mock.MagicMock()
        self.request.session.session_key = None
        self.middleware.process_response(self.request, None)
        self.request.session.cycle_key.assert_called_once()

    def test_response_with_unchanged_session_passes(self):
        self.request.pmetrics_key = self.session_key
        self.middleware.process_response(self.request, None)
        self.request.session.cycle_key.assert_not_called()

    def test_response_with_changed_session_passes(self):
        UserSession.objects.create(session=self.session_key)
        self.request.pmetrics_key = self.session_key[::-1]
        self.assertNotEqual(
            self.request.pmetrics_key,
            self.session.session_key,
            )
        UserSession.objects.create = mock.MagicMock()
        self.middleware.process_response(self.request, None)
        self.request.session.cycle_key.assert_not_called()
        UserSession.objects.create.assert_called_with(
            session=self.request.pmetrics_key,
            user=self.request.user,
            previous_id=self.request.session.session_key,
        )


class MiddlewareWithLoginSignalLoggedInTest(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.middleware = UserSessionTrackingMiddleware()
        self.user = get_user_model().objects.create(username='user')

    def test_user_session_not_duplicated_by_middleware(self):
        self.request.session = Client().session
        UserSession.objects.create(session=self.request.session.session_key)
        self.assertEqual(UserSession.objects.count(), 1)
        self.request.user = self.user
        self.middleware.process_request(self.request)
        self.request.session.cycle_key()
        user_logged_in.send(
            sender=self.__class__,
            request=self.request,
            user=self.user,
            )
        self.assertEqual(UserSession.objects.count(), 2)
        self.middleware.process_response(self.request, None)
        self.assertEqual(UserSession.objects.count(), 2)
