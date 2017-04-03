import datetime

from django.contrib.auth.models import AnonymousUser

from .models import Access


def access_entity(session, user, entity):
    if isinstance(user, AnonymousUser):
        user = None
    return Access.objects.create(
        timestamp=datetime.datetime.now(),
        session_key=session.session_key,
        user=user if user else None,
        action='access',
        resources=['{0}:{1}'.format(entity._meta.db_table, entity.pk)],
    )
