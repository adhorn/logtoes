import uuid
import logging
import boto3
from flask import current_app
import json

try:
    from logtoes.settings import FIREHOSE_STREAM
except ImportError:
    from logtoes.default_settings import FIREHOSE_STREAM


session = boto3.Session()
credentials = session.get_credentials()
# region = os.environ['AWS_REGION']

firehose = boto3.client('firehose')

#  doc_type must be of the format
#  In [24]: doc_type = {'Data': 'value'}


def send_to_firehose(data, doc_type):
    current_app.logger.warning("Data to be sent to firehose {}".format(data))

    response = firehose.put_record(
            DeliveryStreamName=FIREHOSE_STREAM,
            Record={'Data': json.dumps(data) + '\n'}
        )
    return True if response else False
