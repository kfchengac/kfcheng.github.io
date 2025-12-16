"""Trigger a Netlify site build using the Netlify Builds API.

Reads NETLIFY_AUTH_TOKEN and NETLIFY_SITE_ID from the environment.
Prints the created build id and state on success.
"""
import os
import sys
import json

import requests


def main():
    token = os.getenv('NETLIFY_AUTH_TOKEN')
    site_id = os.getenv('NETLIFY_SITE_ID')

    if not token or not site_id:
        print('Missing NETLIFY_AUTH_TOKEN and/or NETLIFY_SITE_ID environment variables.')
        print('Set them and re-run this script. Example:')
        print('  export NETLIFY_AUTH_TOKEN=your_token')
        print('  export NETLIFY_SITE_ID=your_site_id')
        sys.exit(2)

    url = f'https://api.netlify.com/api/v1/sites/{site_id}/builds'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        # You can add "clear_cache": true if needed
        'clear_cache': False
    }

    print('Triggering Netlify build...')
    resp = requests.post(url, headers=headers, json=payload, timeout=30)

    try:
        j = resp.json()
    except Exception:
        print('Non-JSON response, status:', resp.status_code)
        print(resp.text)
        sys.exit(1)

    if resp.status_code in (200, 201):
        print('Build triggered successfully')
        print('Build id:', j.get('id'))
        print('State:', j.get('state'))
        print('Deploy URL (if available):', j.get('deploy_id'))
        print('Full response:')
        print(json.dumps(j, indent=2))
        return 0
    else:
        print('Failed to trigger build. HTTP', resp.status_code)
        print(json.dumps(j, indent=2))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
