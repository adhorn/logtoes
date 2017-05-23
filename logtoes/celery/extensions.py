from celery import Celery

try:
    from logtoes.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
except ImportError:
    from logtoes.default_settings import CELERY_BROKER_URL, \
        CELERY_RESULT_BACKEND


celery = Celery(
    'logtoes',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)


def set_celery(app):
    cel = celery
    cel.conf.update(app.config)
    TaskBase = cel.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    cel.Task = ContextTask
    return cel
