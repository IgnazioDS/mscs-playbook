COMPOSE_FILE := docker-compose.yml
LOCAL_ENV := .env.local.example
PROD_ENV := .env.production.example
VENV_PYTHON ?= python3.11

.PHONY: test compose-config up-local up-prod-like down retention backup-control-plane restore-control-plane load-smoke slo-check

test:
	$(VENV_PYTHON) -m pytest -q tests

compose-config:
	docker compose --env-file $(LOCAL_ENV) -f $(COMPOSE_FILE) config -q

up-local:
	docker compose --env-file $(LOCAL_ENV) -f $(COMPOSE_FILE) up -d --build

up-prod-like:
	docker compose --env-file $(PROD_ENV) -f $(COMPOSE_FILE) up -d --build

down:
	docker compose --env-file $(LOCAL_ENV) -f $(COMPOSE_FILE) down -v --remove-orphans

retention:
	$(VENV_PYTHON) scripts/retention.py

backup-control-plane:
	$(VENV_PYTHON) scripts/backup_control_plane.py --output artifacts/control-plane-backup.json

restore-control-plane:
	$(VENV_PYTHON) scripts/restore_control_plane.py artifacts/control-plane-backup.json

load-smoke:
	$(VENV_PYTHON) scripts/load_harness.py \
		--ingest-key-id local-ingest \
		--ingest-key local-demo-ingest-key \
		--operator-key-id local-ops \
		--operator-key local-demo-ops-key \
		--requests 3 \
		--output artifacts/load-smoke.json

slo-check:
	$(VENV_PYTHON) scripts/slo_check.py \
		--base-url http://localhost:8000 \
		--operator-key-id local-ops \
		--operator-key local-demo-ops-key \
		--capacity-report artifacts/load-smoke.json \
		--readiness-availability 1.0
