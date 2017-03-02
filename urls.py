from .views import ActionViewSet


def register(router):
    router.register(r'actions', ActionViewSet, base_name='action')
