import pygeoip
from flask import current_app
from logtoes.celery.extensions import celery as ce
from logtoes.utils.elastic import send_to_elk


try:
    from logtoes.settings import GEO_FILE, ELASTICSEARCH_ENABLED
except ImportError:
    from logtoes.default_settings import GEO_FILE, ELASTICSEARCH_ENABLED


gi = pygeoip.GeoIP(GEO_FILE, pygeoip.MEMORY_CACHE)


def reverse_geo_ip(ip_address):
    if ip_address:
        geo_data = gi.record_by_addr(ip_address)
        if geo_data is not None:
            return geo_data
    return dict()


@ce.task(bind=True, default_retry_delay=5)
def prep_to_elk(self, data, doc_type):
    ip_address = data['ip']
    location_blob = reverse_geo_ip(ip_address)
    #  The field that contains the coordinates, in geojson format.
    #  GeoJSON is [longitude,latitude] in an array.
    #  Different from most implementations, which use latitude, longitude
    location = [
        float(
            location_blob.get('longitude', '0')
        ), float(
            location_blob.get('latitude', '0')
        )
    ]
    country = '{0}'.format(location_blob.get('country_name', 'unkown'))
    data.update({'location': location})
    data.update({'country': country})

    try:
        current_app.logger.debug(
            "Task: logs to ElasticSearch for use in Kibana:  {}".format(data))

        if ELASTICSEARCH_ENABLED:
            send_to_elk(data, doc_type)
        return True
    except Exception as exc:
            raise self.retry(exc=exc, countdown=5)


@ce.task(bind=True)
def add(self, x, y):
    current_app.logger.debug(
        "Task: Test with {0} and {1} ".format(x, y))
    return x + y
