from flask import current_app

from utilities.constant import FULLTEXT_SEARCH_BIG_NUMBER, DEFAULT_LANGUAGE
from utilities.helper import Utility


def index_to_search(index, doc_type, model):
    # TODO: Move to background jobs
    es = current_app.elasticsearch
    if not es.indices.exists(index):
        settings = model.__mappings__
        es.indices.create(index=index, body=settings)

    payload = model.to_dict()
    current_app.elasticsearch.index(index=index, doc_type=doc_type, id=model.id, body=payload)


def remove_from_index(index, doc_type, model):
    current_app.elasticsearch.delete(index=index, doc_type=doc_type, id=model.id, ignore=404)


def suggest_parser(prefix, suggest_field):
    # TODO: must construct sort field more dynamic instead of hard code
    rv = {
        'query': {
            'match': {
            }
        },
        'sort': [{'slug': {'order': 'asc'}}],
        'from': 0, 'size': FULLTEXT_SEARCH_BIG_NUMBER
    }

    rv['query']['match'][suggest_field] = {
        'query': prefix,
        'operator': 'and'
    }

    return rv


def suggest_completion(indices, prefix, suggest_field, display_language=DEFAULT_LANGUAGE):
    indices_string = ','.join(indices)

    if not current_app.elasticsearch:
        return []

    suggest_body = suggest_parser(prefix, suggest_field)
    search = current_app.elasticsearch.search(index=indices_string, body=suggest_body)

    rv = {index: [] for index in indices}
    for hit in search['hits']['hits']:
        if hit['_index'] not in rv:
            rv[hit['_index']] = []

        value = hit['_source']

        value['text'] = ''
        for text in value['_texts']:
            if text['locale_id'] == display_language:
                value['text'] = text['display_text']

        del value[suggest_field]
        del value['_texts']
        rv[hit['_index']].append(value)

    return rv


def remove_index(index):
    current_app.elasticsearch.indices.delete(index=index, ignore=[400, 404])


def reindex(model):
    for obj in model.query.active().not_deleted().all():
        index_to_search(obj.__tablename__, obj.__tablename__, obj)


def before_commit(session):
    session.changes_ = {
        'add': list(session.new),
        'update': list(session.dirty),
        'delete': list(session.deleted)
    }


def after_commit(session):
    for obj in session.changes_['add']:
        need_index = _is_document(obj) and _need_index(obj)

        if not need_index:
            continue

        index_to_search(obj.__tablename__, obj.__tablename__, obj)

    for obj in session.changes_['update']:
        if not _is_document(obj):
            continue

        need_remove = not _need_index(obj)

        if need_remove:
            remove_from_index(obj.__tablename__, obj.__tablename__, obj)
        else:
            index_to_search(obj.__tablename__, obj.__tablename__, obj)

    for obj in session.changes_['delete']:
        if not _is_document(obj):
            continue

        remove_from_index(obj.__tablename__, obj.__tablename__, obj)

    session.changes_ = None


def _is_document(obj: any) -> bool:
    return hasattr(obj, '__searchable__') and obj.__searchable__


def _need_index(obj: any) -> bool:
    rv = True

    if hasattr(obj, 'is_active') or hasattr(obj, 'is_deleted'):
        rv = Utility.get_attribute(obj, 'is_active') or Utility.get_attribute(obj, 'is_deleted')

    if hasattr(obj, 'publish_to_search'):
        rv = rv & Utility.get_attribute(obj, 'publish_to_search')

    return rv


