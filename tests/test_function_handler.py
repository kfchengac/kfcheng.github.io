import os
import sys
import json

# Ensure repo root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netlify.functions.app import handler


def make_event(path='/', method='GET', body=None):
    event = {
        'httpMethod': method,
        'path': path,
        'rawPath': path,
        'headers': {'Host': 'localhost'},
        'queryStringParameters': None,
        'isBase64Encoded': False,
        'body': None,
        'requestContext': {'http': {'method': method, 'path': path}}
    }
    if body is not None:
        event['body'] = json.dumps(body)
    return event


def test_health_handler():
    event = make_event(path='/health', method='GET')
    resp = handler(event, None)
    assert resp['statusCode'] == 200
    body = json.loads(resp['body'])
    assert 'status' in body and body['status'] == 'ok'


def test_post_chat_handler():
    payload = {'message': 'pytest invocation', 'session_id': 'test', 'history': [], 'persona': 'strategist'}
    event = make_event(path='/api/chat', method='POST', body=payload)
    event['headers'] = {'Content-Type': 'application/json'}
    resp = handler(event, None)
    assert resp['statusCode'] == 200
    body = json.loads(resp['body'])
    assert 'response' in body
