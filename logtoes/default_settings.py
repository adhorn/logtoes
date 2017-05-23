import os
basedir = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1'
URL_PREFIX_VERSION = '/api'

GEO_FILE = 'logtoes/geocity/GeoLiteCity.dat'

HOST = 'localhost'
PORT = 5555
DEBUG = True
BRANCH = 'master'

TRAP_HTTP_EXCEPTIONS = True
TRAP_BAD_REQUEST_ERRORS = True
JSONIFY_PRETTYPRINT_REGULAR = True

ERROR_404_HELP = False

ERROR_TO_FILE = True
ERROR_LOG_NAME = 'logs/errors.log'


CELERY_BROKER_URL = ['redis://localhost:6379/0']
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERYD_LOG_FILE = "logs/celery.log"
CELERY_IGNORE_RESULT = False
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_ENABLE_UTC = True
CELERY_DEFAULT_ROUTING_KEY = "logtoes"
CELERY_DEFAULT_QUEUE = 'logtoes'
CELERY_DEFAULT_EXCHANGE = "logtoes"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['pickle']

BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
BROKER_CONNECTION_MAX_RETRIES = 0
BROKER_FAILOVER_STRATEGY = "round-robin"
BROKER_HEARTBEAT = 10


ELASTICSEARCH_URL = 'localhost'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_INDEX = 'logtoes'
ELASTICSEARCH_MAPPPING = 'logtoes'
ELASTICSEARCH_ENABLED = True


ELASTICSEARCH_SETTINGS = {
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "api_requests": {
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "ip": {
                    "type": "ip"
                },
                "location": {
                    "type": "geo_point"
                },
                "country": {
                    "type": "multi_field",
                    "fields": {
                        "country": {"type": "string", "index": "analyzed"},
                        "untouched": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "user": {
                    "type": "string"
                },
                "request": {
                    "type": "multi_field",
                    "fields": {
                        "request": {"type": "string", "index": "analyzed"},
                        "untouched": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "status code": {
                    "type": "integer"
                },
                "query": {
                    "type": "string"
                },
                "agent": {
                    "type": "multi_field",
                    "fields": {
                        "agent": {"type": "string", "index": "analyzed"},
                        "untouched": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "raw agent": {
                    "type": "multi_field",
                    "fields": {
                        "raw agent": {"type": "string", "index": "analyzed"},
                        "untouched": {"type": "string", "index": "not_analyzed"}
                    }
                }
            }
        }
    }
}

try:
    from local_settings import *
except ImportError:
    pass

try:
    from settings import *
except ImportError:
    pass
