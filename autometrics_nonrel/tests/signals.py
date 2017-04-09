from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.test import RequestFactory
from django.test import TestCase
from django.test.client import Client

from ..models import UserSession


class UserLoggedInTest(TestCase):

    def test_user_session_created_when_user_logs_in(self):
        self.assertEqual(UserSession.objects.count(), 0)
        user = get_user_model().objects.create(username='user')
        request = RequestFactory().get('/')
        request.session = Client().session
        user_logged_in.send(sender=self.__class__, request=request, user=user)
        self.assertEqual(UserSession.objects.count(), 1)
        user_session = UserSession.objects.get()
        self.assertEqual(user_session.user, user)
        self.assertEqual(user_session.session, request.session.session_key)
