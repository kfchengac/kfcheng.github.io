Netlify deployment notes
=======================

This project is a Flask WSGI app. To deploy on Netlify we run the Flask app inside a Netlify Function (AWS Lambda) using awsgi.

What was added
- netlify.toml — config that points functions to netlify/functions and redirects all requests to the function.
- netlify/functions/app.py — a small wrapper which forwards incoming requests to the Flask app using awsgi.
- public/static/* — copies of frontend static assets so Netlify can serve them from the publish directory (faster CDN delivery).
- awsgi added to requirements.txt so Netlify installs the wrapper dependency.

Important environment variables
- SECRET_KEY — Flask session secret. Set in Netlify site settings (Environment -> Environment variables).
- OPENAI_API_KEY — required if you enable the OpenAI API mode in admin settings.
- CORS_ORIGINS (optional) — comma-separated origins.

CI / Auto-deploy secrets (GitHub)
- NETLIFY_AUTH_TOKEN — Personal Access Token for Netlify (create in Netlify user settings). Add this as a GitHub repo secret.
- NETLIFY_SITE_ID — Your Netlify Site ID (found in Site settings -> Site information). Add this as a GitHub repo secret.

The CI workflow includes a step that will POST to the Netlify Builds API to trigger a site build after the smoke tests pass. Add the two secrets above in your repository Settings -> Secrets -> Actions before enabling automatic deploys.

Python runtime
- The project has runtime.txt pinned to python-3.12.3. Netlify uses the system Python; if you change runtime, update this file.

How Netlify routes requests
- All incoming requests are redirected (status 200) to /.netlify/functions/app by netlify.toml. The function uses awsgi to run the Flask app and return responses.

Notes & caveats
- Long-running tasks (like heavy lead generation or external scraping) may time out on Netlify Functions (Lambda time limit). For heavy background jobs, consider using an external worker (e.g., AWS Lambda with longer timeout, Cloud Run, or a background job service).
- The admin interface is still rendered server-side by Flask; sessions are maintained via Flask session cookies backed by SECRET_KEY.
- Static assets are copied to public/static/; if you change files in static/ remember to sync them to public/static/ before deploying.

Deploy steps (quick)
1. In Netlify UI, create a new site from the repo (connect Git provider) or drag-and-drop the repository.
2. In Site settings -> Build & deploy -> Environment, add environment variables SECRET_KEY and OPENAI_API_KEY (if needed).
3. Verify netlify.toml is present at repo root and requirements.txt includes awsgi.
4. Push to the main branch. Netlify will install dependencies and build functions. The site will be published from the public/ directory and all requests will be routed to the app function.

Local testing
----------------
You can test the function locally using the Netlify CLI (optional):

Install Netlify CLI: npm i -g netlify-cli
Run locally from repo root: netlify dev

Local dev helper
- `scripts/local_dev.sh` will try to start `netlify dev` in the background, wait for the server to be ready, run the smoke tests, and tail logs. Usage:

```bash
# make sure you installed netlify cli
npm i -g netlify-cli
# install python deps
python3 -m pip install -r requirements.txt
# run helper (optional specify PORT)
./scripts/local_dev.sh
```

If you don't use Netlify CLI, you can still run the Flask app locally with:

python app.py

Next steps (optional)
- Sync any remaining static/ assets to public/static/ or create a small build script to copy them at build time.
- Add small wrapper tests for the functions to verify basic endpoints (/health, /api/chat).
 - CI now includes unit tests (pytest) and a Netlify build poll step. Ensure you add `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` as GitHub repo secrets to enable auto-deploys.

CI / Deploy checklist (exact secrets & variables)
------------------------------------------------
- NETLIFY_AUTH_TOKEN — Personal access token created in your Netlify user settings (Account -> User settings -> Applications). Add as a GitHub Actions repository secret named `NETLIFY_AUTH_TOKEN`.
- NETLIFY_SITE_ID — Netlify Site ID (Site settings -> Site information). Add as a GitHub Actions repository secret named `NETLIFY_SITE_ID`.
- REDIS_URL — Redis connection URL used by RQ workers (example: `redis://redis:6379` or `redis://:password@host:6379/0`). Add this to the environment where workers run (not required on Netlify functions).
- OPENAI_API_KEY — (optional) If you enable OpenAI API mode in the admin UI, set this in Netlify Environment variables or in the worker host environment.
- SECRET_KEY — Flask secret key for session cookies. Set in Netlify Environment variables (recommended) or in the worker host.

Notes:
- The GitHub Actions workflow included in `.github/workflows/ci.yml` will run tests and then trigger a Netlify build via the Netlify Builds API using `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID`.
- The Netlify Function wrapper runs the Flask WSGI app inside a Lambda-like environment — it is suitable for request/response flows but not for long-running background work. Use `REDIS_URL` + a separate RQ worker for background processing.
Compatibility note — awsgi
--------------------------------
The Netlify wrapper originally used `awsgi.response` to convert AWS proxy events into WSGI requests. Different `awsgi` releases expose different adapters. During development we pinned `awsgi==0.0.5` which works in this repo and provides a lightweight adapter, but some environments may provide a different `awsgi` API.

To make the function wrapper robust across awsgi versions, the wrapper includes a fallback path that uses Flask's `test_request_context` to dispatch requests when `awsgi.response` is not available. This ensures the function handler works locally and on Netlify even if awsgi in the environment differs.

Recommendation:
- Keep `awsgi` pinned in `requirements.txt` for reproducible builds (this repo uses `awsgi==0.0.5`).
- The compatibility fallback in `netlify/functions/app.py` will handle mismatches, so the function should still work if Netlify's build environment uses a different awsgi release.

Background worker (optional)
- A simple SQLite-backed job queue and worker have been added. Use `POST /api/lead-gen/queue` to enqueue a campaign and `GET /api/lead-gen/job/<job_id>` to check status.
- Run the worker on a separate host (not Netlify) with:

Recommended worker options (Redis + RQ) — production-ready
---------------------------------------------------------
Prefer running RQ workers on a separate host or container (not Netlify). We've included a `docker-compose.yml` that starts Redis and a worker image for local testing.

Local Docker Compose (recommended for local dev):

```bash
# start redis + worker
docker-compose up -d

# point your app/worker to Redis (example for local):
export REDIS_URL=redis://localhost:6379

# run an RQ worker (alternative to docker-compose worker):
python3 -m rq worker --with-scheduler default
```

Or using the provided helper (if present):

```bash
./scripts/start_rq_worker.sh
```

If you prefer a simple Python worker (SQLite fallback) it's present as `scripts/worker.py` but note:
- SQLite worker is intended only for local testing and small workloads. For reliability and scale use Redis + RQ.

Troubleshooting & verification
------------------------------
- Run the Flask test-client smoke test (no server required):

```bash
PYTHONPATH=. python3 scripts/smoke_test_client.py
```

- To test the Netlify Function wrapper locally with Netlify CLI:

```bash
npm i -g netlify-cli
netlify dev
# then visit: http://localhost:8888/.netlify/functions/app/health
```

Final notes
-----------
- Add the GitHub Actions secrets `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` to enable CI-triggered Netlify deploys. Also make sure any runtime secrets (OPENAI_API_KEY, SECRET_KEY, REDIS_URL) are configured in the environment where they are needed (Netlify site settings for function runtime; your worker host for REDIS_URL).
- If you'd like, I can prepare a small GitHub Actions PR that adds a step to verify secrets are present before triggering a Netlify build, and a short dashboard README for running the worker in production (systemd/service or Docker Compose instructions).

Temporary debug build (optional)
--------------------------------
If Netlify deploys static files but reports "No functions deployed" or the build log says "No build steps found", you can use the included debug build helper to expose what the build container actually sees.

What to do:

1. Ensure `netlify.toml`, `netlify/functions/` and `scripts/netlify_build_debug.sh` are committed on the branch Netlify builds.
2. Push the branch or trigger a redeploy in the Netlify UI.
3. Inspect the build log — the debug script prints a root listing, `netlify/functions/` listing, and a short head of each `.py` function file so you can verify functions are present.

When finished debugging, revert `netlify.toml`'s `build.command` to a shorter command (for example `python3 scripts/sync_static.py`) so subsequent builds are concise.
