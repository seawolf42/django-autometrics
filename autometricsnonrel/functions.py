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
        model=entity._meta.db_table,
        ids=[entity.pk],
    )


def list_entities(session, user, entities):
    if isinstance(user, AnonymousUser):
        user = None
    return Access.objects.create(
        timestamp=datetime.datetime.now(),
        session_key=session.session_key,
        user=user if user else None,
        action='list',
        model=entities[0]._meta.db_table,
        ids=[entity.pk for entity in entities],
    )
