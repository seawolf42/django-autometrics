import mock
from funcsigs import signature

from django.test import TestCase

from ..mixins import RestFrameworkGenericViewSetAutoMetricsMixin


dummy_object = object()


class DummyGenericViewSet(object):

    def get_object(self):
        return dummy_object


class RestFrameworkGenericViewSetMetricsMixinTest(TestCase):

    def setUp(self):
        self.session = 'session'
        self.user = 'user'
        self.request = mock.MagicMock()
        self.request.session = self.session
        self.request.user = self.user

    def test_mixin_has_get_object_method(self):
        mixin = RestFrameworkGenericViewSetAutoMetricsMixin()
        function = getattr(mixin, 'get_object')
        self.assertTrue(callable(function))
        self.assertEqual(len(signature(function).parameters), 0)

    def test_viewset_get_object(self):
        import autometrics_nonrel.mixins as m
        m.get_entity = mock.MagicMock()

        class DummyViewSet(
                RestFrameworkGenericViewSetAutoMetricsMixin,
                DummyGenericViewSet,
                ):
            pass
        viewset = DummyViewSet()
        viewset.request = self.request
        result = viewset.get_object()
        self.assertEqual(result, dummy_object)
        m.get_entity.assert_called_once()
        m.get_entity.assert_called_with(
            self.session,
            self.user,
            dummy_object,
            )
