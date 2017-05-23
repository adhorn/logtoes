import os
import logging
import uuid
import datetime
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler


def get_datetime():
    now = datetime.datetime.utcnow()
    return str(now.replace(microsecond=0))


def generate_uuid():
    return str(uuid.uuid4()).replace('-', '')


def create_path_if_not_exist(path_and_file):
    path, _ = os.path.split(path_and_file)
    if not os.path.exists(path):
        os.makedirs(path)
    return path_and_file


def configure_logging(app):
    if app.config['ERROR_TO_FILE']:
        error_log_name = app.config['ERROR_LOG_NAME']
        file_handler = TimedRotatingFileHandler(
            filename=create_path_if_not_exist(error_log_name),
            when='d')
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
        ))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('logtoes startup')
