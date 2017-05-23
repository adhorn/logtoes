from flask import current_app, g, request, jsonify
from functools import wraps
import json
from datetime import datetime
from logtoes.celery import tasks


def api_error_response(code=404, message="Resource not found", errors=list()):
    response = jsonify(
        dict(code=code, message=message, errors=errors, success=False))
    response.status_code = code
    return response


def bad_json_error_response():
    return api_error_response(
        code=400,
        message="Please provide valid JSON."
    )


class ModelJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return json.JSONEncoder.default(self, obj)


def json_response(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(result, current_app.response_class):
            return result
        if isinstance(result, (list, tuple)):
            result = {'items': result}
        data = json.dumps(result, cls=ModelJSONEncoder)
        return current_app.response_class(data, mimetype='application/json')
    return wrapped


def log_entry(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        result = fn(*args, **kwargs)
        status_code = result.status_code
        auth_user = "guest"
        if request.authorization:
            auth_user = request.authorization.username
            if request.authorization.password == 'unused':
                auth_user = g.user.verify_auth_token(
                    request.authorization.username).username

        ip_address = request.environ.get('HTTP_X_FORWARDED_HOST')
        if not ip_address:
            ip_address = request.environ.get('REMOTE_ADDR', '0.0.0.0')
        if ip_address:
            ip_address = ip_address.split(',')[0]

        data = {
            'user': '{}'.format(auth_user),
            'request': '{0} {1}'.format(request.method, request.path),
            'status code': '{}'.format(status_code),
            'query': '{}'.format(request.query_string),
            'ip': '{}'.format(ip_address),
            'agent': '{0} | {1} {2}'.format(
                request.user_agent.platform,
                request.user_agent.browser,
                request.user_agent.version),
            'raw agent': '{}'.format(request.user_agent.string),
            '@timestamp': datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S")
        }

        tasks.prep_to_elk.delay(data, 'api_requests')
        current_app.logger.debug(
            """
User:       {user}
Request:    {method} {path}
Code:       {status_code}
Query:      {query}
IP:         {ip}
Agent:      {agent_platform} | {agent_browser} {agent_browser_version}
Raw Agent:  {agent}
Time:       {time}
Args:       {args}
Kwargs:     {kwargs}
            """.format(method=request.method,
                       query=request.query_string,
                       status_code=status_code,
                       path=request.path,
                       ip=ip_address,
                       agent_platform=request.user_agent.platform,
                       agent_browser=request.user_agent.browser,
                       agent_browser_version=request.user_agent.version,
                       agent=request.user_agent.string,
                       user=auth_user,
                       time=datetime.utcnow(),
                       args=dict(request.args or []),
                       kwargs=dict(**kwargs or {}),
                       )
        )
        return result
    return wrapped
