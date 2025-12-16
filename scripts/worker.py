#!/usr/bin/env python3
"""Background worker to process queued lead generation jobs from jobs.db.

Run this on a machine with the repo checked out (not on Netlify Functions).
"""
import time
import sqlite3
import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT, 'jobs.db')

from lead_gen import LeadGenerator

SLEEP_SECONDS = 5


def fetch_pending_job(conn):
    c = conn.cursor()
    c.execute("SELECT id, job_id, payload FROM jobs WHERE status = 'pending' ORDER BY id LIMIT 1")
    row = c.fetchone()
    return row


def mark_in_progress(conn, id):
    now = datetime.now().isoformat()
    c = conn.cursor()
    c.execute("UPDATE jobs SET status = 'in_progress', updated_at = ? WHERE id = ?", (now, id))
    conn.commit()


def mark_done(conn, id, result):
    now = datetime.now().isoformat()
    c = conn.cursor()
    c.execute("UPDATE jobs SET status = 'done', updated_at = ?, result = ? WHERE id = ?", (now, json.dumps(result), id))
    conn.commit()


def mark_failed(conn, id, error):
    now = datetime.now().isoformat()
    c = conn.cursor()
    c.execute("UPDATE jobs SET status = 'failed', updated_at = ?, result = ? WHERE id = ?", (now, json.dumps({'error': str(error)}), id))
    conn.commit()


def process_job(job_row):
    id, job_id, payload_json = job_row
    payload = json.loads(payload_json or '{}')
    generator = LeadGenerator()

    # Extract expected fields with defaults
    instagram_hashtags = payload.get('instagram_hashtags', [])
    linkedin_keywords = payload.get('linkedin_keywords', [])
    max_leads = int(payload.get('max_leads', 50))
    auto_outreach = payload.get('auto_outreach', False)

    results = generator.run_lead_generation_campaign(
        instagram_hashtags=instagram_hashtags,
        linkedin_keywords=linkedin_keywords,
        max_leads=max_leads,
        auto_outreach=auto_outreach
    )

    return results


def main():
    print('Starting worker — watching for jobs in', DB_PATH)
    while True:
        conn = sqlite3.connect(DB_PATH)
        row = fetch_pending_job(conn)
        if not row:
            conn.close()
            time.sleep(SLEEP_SECONDS)
            continue

        id = row[0]
        try:
            mark_in_progress(conn, id)
            print('Processing job id', id)
            result = process_job(row)
            mark_done(conn, id, result)
            print('Job done', id)
        except Exception as e:
            print('Job failed', id, str(e))
            mark_failed(conn, id, e)
        finally:
            conn.close()


if __name__ == '__main__':
    main()
