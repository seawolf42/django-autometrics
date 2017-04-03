import datetime

from django.contrib.auth.models import AnonymousUser

from .models import Access


def get_entity(session, user, entity):
    if isinstance(user, AnonymousUser):
        user = None
    return Access.objects.create(
        timestamp=datetime.datetime.now(),
        session_key=session.session_key,
        user=user if user else None,
        action='get',
        model=entity._meta.db_table,
        ids=[entity.pk],
    )


def get_entity_list(session, user, entities):
    if isinstance(user, AnonymousUser):
        user = None
    if len(entities) == 0:
        return None
    for e in entities[1:]:
        assert(e.__class__ == entities[0].__class__)
    return Access.objects.create(
        timestamp=datetime.datetime.now(),
        session_key=session.session_key,
        user=user if user else None,
        action='list',
        model=entities[0]._meta.db_table,
        ids=[entity.pk for entity in entities],
    )
