"""Invoke the Netlify function handler directly with a proxy GET event.

This avoids needing Netlify CLI and tests the awsgi wrapper -> Flask app path.
"""
import json
import os
import sys

# Ensure project root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netlify.functions.app import handler


def make_event(path='/.netlify/functions/app/health', method='GET'):
    return {
        'httpMethod': method,
        'path': path,
        'rawPath': path,
        'headers': {
            'Host': 'localhost'
        },
        'queryStringParameters': None,
        'isBase64Encoded': False,
        'body': None,
        'requestContext': {
            'http': {'method': method, 'path': path}
        }
    }


def main():
    print('Invoking Netlify function handler for /health')
    event = make_event(path='/health', method='GET')
    resp = handler(event, None)
    print('GET /health ->', resp.get('statusCode'))
    try:
        print('Body JSON:', json.dumps(json.loads(resp.get('body')), indent=2))
    except Exception:
        print('Body:', resp.get('body'))

    # POST test to /api/chat
    print('\nInvoking Netlify function handler for POST /api/chat')
    payload = {'message': 'Hello from function-invoke', 'session_id': 'fn_test', 'history': [], 'persona': 'strategist'}
    post_event = make_event(path='/api/chat', method='POST')
    post_event['headers'] = {'Content-Type': 'application/json'}
    post_event['body'] = json.dumps(payload)
    post_event['isBase64Encoded'] = False
    resp2 = handler(post_event, None)
    print('POST /api/chat ->', resp2.get('statusCode'))
    try:
        print('Body JSON:', json.dumps(json.loads(resp2.get('body')), indent=2))
    except Exception:
        print('Body:', resp2.get('body'))


if __name__ == '__main__':
    main()
