import mock
from funcsigs import signature
from collections import OrderedDict

from django.test import TestCase

from ..mixins import RestFrameworkGenericViewSetAutoMetricsMixin


dummy_object = object()
dummy_list = [
    OrderedDict([('id', 123), ('value', 'abc')]),
    OrderedDict([('id', 456), ('value', 'def')]),
]
dummy_list_ids = [x['id'] for x in dummy_list]
dummy_list_response = mock.MagicMock()
dummy_list_response.data = {
    'results': dummy_list
}


class DummyGenericViewSet(object):

    def get_object(self):
        return dummy_object

    def list(self, request, *args, **kwargs):
        return dummy_list_response

    def get_queryset(self):
        queryset = mock.MagicMock()
        queryset.model._meta.db_table = 'entity_model'
        return queryset


class RestFrameworkGenericViewSetMetricsMixinTest(TestCase):

    class DummyViewSet(
            RestFrameworkGenericViewSetAutoMetricsMixin,
            DummyGenericViewSet,
            ):
        pass

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
        viewset = self.DummyViewSet()
        viewset.request = self.request
        result = viewset.get_object()
        self.assertEqual(result, dummy_object)
        m.get_entity.assert_called_once()
        m.get_entity.assert_called_with(
            self.session,
            self.user,
            dummy_object,
            )

    def test_mixin_has_list_method(self):
        mixin = RestFrameworkGenericViewSetAutoMetricsMixin()
        function = getattr(mixin, 'list')
        self.assertTrue(callable(function))
        self.assertEqual(len(signature(function).parameters), 3)
        self.assertIsNotNone(signature(function).parameters['request'])
        self.assertIsNotNone(signature(function).parameters['args'])
        self.assertIsNotNone(signature(function).parameters['kwargs'])

    def test_viewset_list(self):
        import autometrics_nonrel.mixins as m
        m.get_entity_id_list = mock.MagicMock()
        viewset = self.DummyViewSet()
        viewset.request = self.request
        viewset.list(self.request)
        m.get_entity_id_list.assert_called_once()
        m.get_entity_id_list.assert_called_with(
            self.session,
            self.user,
            'entity_model',
            dummy_list_ids,
            )
