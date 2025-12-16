#!/usr/bin/env python3
"""Poll Netlify build status until completion.

Usage:
  python3 scripts/netlify_poll.py <site_id> <build_id> <auth_token> [--timeout-seconds=300]

This script will poll the Netlify Builds API and print final build status.
Exit code 0 on success (ready), non-zero on failure or timeout.
"""
import sys
import time
import requests
import json


def usage_and_exit():
    print(__doc__)
    sys.exit(2)


def main():
    if len(sys.argv) < 4:
        usage_and_exit()

    site_id = sys.argv[1]
    build_id = sys.argv[2]
    token = sys.argv[3]
    timeout = 300
    for arg in sys.argv[4:]:
        if arg.startswith('--timeout-seconds='):
            timeout = int(arg.split('=', 1)[1])

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f'https://api.netlify.com/api/v1/sites/{site_id}/builds/{build_id}'
    start = time.time()
    while True:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print('Failed to fetch build status:', r.status_code, r.text)
            sys.exit(3)

        j = r.json()
        state = j.get('state')
        print('Build state:', state)
        if state == 'ready':
            print('Build finished successfully')
            sys.exit(0)
        if state in ('error', 'cancelled'):
            print('Build failed with state:', state)
            print(json.dumps(j, indent=2))
            sys.exit(4)

        if time.time() - start > timeout:
            print('Timeout waiting for build to finish')
            sys.exit(5)

        time.sleep(5)


if __name__ == '__main__':
    main()
