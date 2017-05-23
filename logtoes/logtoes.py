from __future__ import absolute_import
from gevent.monkey import patch_all, patch_time
patch_all()
patch_time()

from flask import Flask
from logtoes.utils.util import configure_logging
from logtoes.api.echo_api import echo_api
from logtoes.default_settings import URL_PREFIX_VERSION
from logtoes.celery.extensions import celery


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object('logtoes.default_settings')
    if config_module:
        app.config.from_object(config_module)
    app.config.from_envvar('LOGFREE_SETTINGS', silent=True)
    configure_logging(app)
    app.register_blueprint(echo_api, url_prefix=URL_PREFIX_VERSION)
    app.logger.info("Flask App Ready To Go")
    celery.config_from_object(app.config)
    return app

app = create_app()

HOST = app.config['HOST']
PORT = app.config['PORT']

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

# celery -A run_celery worker -l debug -P gevent
# gunicorn -w 1 -b 0.0.0.0:5555 -k gevent logtoes.logtoes:app --reload
