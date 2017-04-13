import datetime

from .models import Access


def get_entity(session, user, entity):
    if user is not None and user.is_anonymous():
        user = None
    return Access.objects.create(
        timestamp=datetime.datetime.now(),
        session_key=session.session_key,
        user=user if user else None,
        action='get',
        model=entity._meta.db_table,
        ids=[entity.pk],
    )


def get_entity_id_list(session, user, model, ids):
    if len(ids) == 0:
        return None
    if user is not None and user.is_anonymous():
        user = None
    return Access.objects.create(
        timestamp=datetime.datetime.now(),
        session_key=session.session_key,
        user=user if user else None,
        action='list',
        model=model,
        ids=ids,
    )


def get_entity_list(session, user, entities):
    if len(entities) == 0:
        return None
    cls = entities[0].__class__
    for e in entities[1:]:
        assert(e.__class__ == cls)
    return get_entity_id_list(
        session,
        user,
        entities[0]._meta.db_table,
        [entity.pk for entity in entities],
    )
