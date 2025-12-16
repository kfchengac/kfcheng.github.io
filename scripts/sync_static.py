"""Sync static assets into public/static for Netlify publish.

Usage: python3 scripts/sync_static.py
This will remove public/static if present and copy static/ -> public/static.
"""
import shutil
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, 'static')
DST_DIR = os.path.join(ROOT, 'public')
DST = os.path.join(DST_DIR, 'static')

if not os.path.exists(SRC):
    print(f"Source static directory not found: {SRC}")
    sys.exit(1)

os.makedirs(DST_DIR, exist_ok=True)

# Remove existing dst if present
if os.path.exists(DST):
    print(f"Removing existing {DST}")
    shutil.rmtree(DST)

print(f"Copying static from {SRC} to {DST}")
shutil.copytree(SRC, DST)
print("Static sync complete.")
