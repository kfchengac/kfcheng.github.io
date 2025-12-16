"""Netlify Function wrapper for the Flask app using awsgi.

This file exposes a `handler(event, context)` function which Netlify will invoke.
It forwards incoming Lambda proxy events to the Flask WSGI app using `awsgi`.
"""
import os
import sys
import logging
import json

# Ensure the project root is on the path so `app` can be imported
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# When running on Netlify, we want Flask to serve static files from the publish
# directory (`public/static`). Set the environment variable before importing the
# Flask app so the app will pick it up.
os.environ.setdefault('FLASK_STATIC_FOLDER', 'public/static')
os.environ.setdefault('FLASK_TEMPLATE_FOLDER', 'templates')

from app import app as flask_app  # import the Flask app defined in app.py
import awsgi

logger = logging.getLogger(__name__)
logger.info('Netlify function app wrapper initialized')


def handler(event, context):
    """AWS Lambda handler invoked by Netlify Functions.

    Netlify passes AWS proxy-compatible events to Python functions. `awsgi.response`
    will convert the Flask WSGI response into the proper Lambda proxy return value.
    """
    # Prefer awsgi.response when available (older/newer awsgi versions).
    try:
        if hasattr(awsgi, 'response'):
            return awsgi.response(flask_app, event, context)
    except Exception:
        logger.exception('Error calling awsgi.response')

    # Fallback: run the Flask app in a test request context and return a Lambda-style proxy response.
    try:
        path = event.get('rawPath') or event.get('path') or '/'
        method = event.get('httpMethod', 'GET')
        headers = event.get('headers') or {}
        qs = event.get('queryStringParameters') or {}
        body = event.get('body')
        if event.get('isBase64Encoded') and body:
            import base64
            body = base64.b64decode(body)

        # Use Flask test_request_context to dispatch the request
        with flask_app.test_request_context(path=path, method=method, headers=headers, data=body, query_string=qs):
            resp = flask_app.full_dispatch_request()
            response_body = resp.get_data(as_text=True)
            response_headers = {k: v for k, v in resp.headers.items()}
            return {
                'statusCode': resp.status_code,
                'headers': response_headers,
                'body': response_body
            }
    except Exception:
        logger.exception('Fallback function adapter error')
        return {
            'statusCode': 502,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal function error'})
        }
