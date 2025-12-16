PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: sync static sync-static test ci run

sync-static:
	$(PYTHON) scripts/sync_static.py

install-deps:
	$(PIP) install -r requirements.txt

run:
	# Run Flask app locally (same as `python app.py`)
	$(PYTHON) app.py

gunicorn:
	# Run via gunicorn on 127.0.0.1:5001
	gunicorn -w 1 -b 127.0.0.1:5001 app:app

test:
	# Run smoke tests against local server (set SERVER_URL to override)
	$(PYTHON) scripts/smoke_test.py

ci: sync-static install-deps
	# Start gunicorn in background for CI, run smoke tests
	# Note: in CI we background the server; the workflow must ensure backgrounding works
	nohup gunicorn -w 1 -b 127.0.0.1:5001 app:app > /tmp/gunicorn.log 2>&1 &
	$(PYTHON) scripts/smoke_test.py

worker:
	# Run the background worker which processes queued lead-gen jobs
	# If REDIS_URL is configured, prefer RQ worker
	if [ -n "${REDIS_URL-}" ]; then \
		./scripts/start_rq_worker.sh; \
	else \
		$(PYTHON) scripts/worker.py; \
	fi
