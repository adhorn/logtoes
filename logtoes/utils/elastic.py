import uuid
from flask import current_app
from elasticsearch import Elasticsearch

try:
    from logtoes.settings import ELASTICSEARCH_URL, ELASTICSEARCH_INDEX, \
        ELASTICSEARCH_ENABLED, ELASTICSEARCH_SETTINGS
except ImportError:
    from logtoes.default_settings import ELASTICSEARCH_URL, \
        ELASTICSEARCH_INDEX, ELASTICSEARCH_ENABLED, ELASTICSEARCH_SETTINGS


def send_to_elk(data, doc_type):
    if ELASTICSEARCH_ENABLED:
        try:
            es = Elasticsearch([{'host': ELASTICSEARCH_URL}])

            es.indices.create(
                index=ELASTICSEARCH_INDEX,
                ignore=400,
                body=ELASTICSEARCH_SETTINGS
            )
            res = es.index(
                index=ELASTICSEARCH_INDEX,
                doc_type=doc_type,
                id=str(uuid.uuid4().hex),
                body=data)
            return res
        except Exception as exc:
            current_app.logger.warning("Elasticsearch no found {}".format(exc))
            return True
    else:
        return True
