from .views import AccessViewSet


def register(router):
    router.register(r'access', AccessViewSet, base_name='access')
