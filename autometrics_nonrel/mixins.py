from functions import get_entity
from functions import get_entity_id_list


class RestFrameworkGenericViewSetAutoMetricsMixin(object):

    def get_object(self):
        item = super(
            RestFrameworkGenericViewSetAutoMetricsMixin,
            self,
            ).get_object()
        get_entity(self.request.session, self.request.user, item)
        return item

    def list(self, request, *args, **kwargs):
        response = super(
            RestFrameworkGenericViewSetAutoMetricsMixin,
            self,
            ).list(request, *args, **kwargs)
        get_entity_id_list(
            self.request.session,
            self.request.user,
            self.get_queryset().model._meta.db_table,
            [x['id'] for x in response.data['results']],
            )
        return response
