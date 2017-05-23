from __future__ import absolute_import
from logtoes.logtoes import create_app


app = create_app()

HOST = app.config['HOST']
PORT = app.config['PORT']

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)


# gunicorn -w 1 -b 0.0.0.0:5555 -k gevent logtoes.logtoes:app
