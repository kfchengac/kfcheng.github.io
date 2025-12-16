"""Run smoke tests by importing the Flask app and using test_client().

This avoids starting an HTTP server and is suitable for CI/local checks.
"""
import sys
import json
from app import app


def fail(msg):
    print('FAIL:', msg)
    sys.exit(2)


def main():
    print('Running smoke tests via Flask test_client')
    client = app.test_client()

    # health
    r = client.get('/health')
    if r.status_code != 200:
        fail(f'/health returned {r.status_code}: {r.data.decode()}')
    print('/health OK:', r.json)

    # chat
    payload = {'message': 'Hello from smoke test client', 'session_id': 'smoke_test', 'history': [], 'persona': 'strategist'}
    r = client.post('/api/chat', json=payload)
    if r.status_code != 200:
        fail(f'/api/chat returned {r.status_code}: {r.data.decode()}')

    j = r.get_json()
    if 'response' not in j:
        fail(f'/api/chat response JSON missing "response": {j}')

    print('/api/chat OK — sample response length', len(j.get('response', '')))
    print('SMOKE TESTS PASSED')


if __name__ == '__main__':
    main()
