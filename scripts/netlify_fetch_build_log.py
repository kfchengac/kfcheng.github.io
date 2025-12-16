#!/usr/bin/env python3
"""Fetch Netlify build logs for a build and print them to stdout.

Usage: python3 scripts/netlify_fetch_build_log.py <site_id> <build_id> <auth_token>
"""
import sys
import requests

if len(sys.argv) < 4:
    print(__doc__)
    sys.exit(2)

site_id = sys.argv[1]
build_id = sys.argv[2]
token = sys.argv[3]

headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
}

# Try to fetch the build logs via Netlify API
url = f'https://api.netlify.com/api/v1/sites/{site_id}/builds/{build_id}/log'
print('Fetching', url)
resp = requests.get(url, headers=headers)
if resp.status_code != 200:
    print('Failed to fetch build log:', resp.status_code, resp.text)
    sys.exit(3)

print('--- BUILD LOG START ---')
print(resp.text)
print('--- BUILD LOG END ---')
sys.exit(0)
