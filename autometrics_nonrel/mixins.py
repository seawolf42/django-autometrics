from functions import get_entity


class RestFrameworkGenericViewSetAutoMetricsMixin(object):

    def get_object(self):
        item = super(
            RestFrameworkGenericViewSetAutoMetricsMixin,
            self,
            ).get_object()
        get_entity(self.request.session, self.request.user, item)
        return item
