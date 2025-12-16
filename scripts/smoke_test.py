"""Simple smoke tests for local server.

This script expects the app to be reachable at the URL given by the
SERVER_URL environment variable (default: http://127.0.0.1:5001).

It checks /health (GET) and /api/chat (POST) and exits with non-zero
code on failures.
"""
import os
import sys
import requests

SERVER = os.getenv('SERVER_URL', 'http://127.0.0.1:5001')


def fail(msg):
    print('FAIL:', msg)
    sys.exit(2)


def main():
    print('Running smoke tests against', SERVER)

    # health
    try:
        r = requests.get(f'{SERVER}/health', timeout=5)
    except Exception as e:
        fail(f'/health request failed: {e}')

    if r.status_code != 200:
        fail(f'/health returned {r.status_code}: {r.text}')

    print('/health OK:', r.json())

    # chat
    payload = {'message': 'Hello from smoke test', 'session_id': 'smoke_test', 'history': [], 'persona': 'strategist'}
    try:
        r = requests.post(f'{SERVER}/api/chat', json=payload, timeout=10)
    except Exception as e:
        fail(f'/api/chat request failed: {e}')

    if r.status_code != 200:
        fail(f'/api/chat returned {r.status_code}: {r.text}')

    j = r.json()
    if 'response' not in j:
        fail(f'/api/chat response JSON missing "response": {j}')

    print('/api/chat OK — sample response length', len(j.get('response', '')))
    print('SMOKE TESTS PASSED')


if __name__ == '__main__':
    main()
