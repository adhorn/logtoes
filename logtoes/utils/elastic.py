import uuid
import logging
import boto3
from flask import current_app
from elasticsearch import Elasticsearch, RequestsHttpConnection

try:
    from logtoes.settings import ELASTICSEARCH_URL, ELASTICSEARCH_INDEX, \
        ELASTICSEARCH_ENABLED, ELASTICSEARCH_SETTINGS
except ImportError:
    from logtoes.default_settings import ELASTICSEARCH_URL, \
        ELASTICSEARCH_INDEX, ELASTICSEARCH_ENABLED, ELASTICSEARCH_SETTINGS

from requests_aws4auth import AWS4Auth

host = ELASTICSEARCH_URL

session = boto3.Session()
credentials = session.get_credentials()
# region = os.environ['AWS_REGION']

awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    'eu-west-1',
    'es',
    session_token=credentials.token
)

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


# es = Elasticsearch([
#     {'host': ELASTICSEARCH_URL},
# ])

if ELASTICSEARCH_ENABLED:
    try:
        es.indices.create(
            index=ELASTICSEARCH_INDEX,
            ignore=400,
            body=ELASTICSEARCH_SETTINGS
        )
    except Exception as exc:
        logging.warning("Elasticsearch not found {}".format(exc))
        pass


def send_to_elk(data, doc_type):
    if ELASTICSEARCH_ENABLED:
        try:
            res = es.index(
                index=ELASTICSEARCH_INDEX,
                doc_type=doc_type,
                id=str(uuid.uuid4().hex),
                body=data)
            return res
        except Exception as exc:
            current_app.logger.warning("Elasticsearch not found {}".format(exc))
            return True
    else:
        return True
