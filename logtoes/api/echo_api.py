from flask import Blueprint, current_app
from flask.ext.restful import Api, Resource
from logtoes.utils.api_utils import json_response, log_entry

echo_api = Blueprint('echo_api', __name__)
api = Api(echo_api, catch_all_404s=True)


class Echo(Resource):
    method_decorators = [
        json_response,
        log_entry
    ]

    def get(self):
        current_app.logger.info("Calling Echo")
        return {
            "Application Status": "Surprising, but I am up and running!",
        }


api.add_resource(Echo, '/echo')
