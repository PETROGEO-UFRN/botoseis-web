# *** Makefile for building and managing Docker services

.PHONY: build-db build-server build-workspace build-data-view up-default \
				adm build-admin up-admin \
        build-test-db up-test-db upgrade-test-db \
        test \
				build-local-demo up-local-demo \
				agent

FLASK_APP := app.main
TEST_DATABASE_PORT := 5431

# *** Default targets, production like build (end user only, no admin module)
default: build-db build-server build-workspace build-data-view up-default

build-db:
	docker compose build db

build-server:
	docker compose build server

build-workspace:
	docker compose build workspace

build-data-view:
	docker compose build data-view

up-default:
	@echo "Starting default services..."
	docker compose up db server workspace data-view -d

# *** Admin module and dependencies. 
adm: build-db build-server build-admin up-admin

build-admin:
	docker compose build admin

up-admin:
	@echo "Starting admin service and dependencies..."
	docker compose up db server admin -d

# *** Full demo in dedicated docker-stack
# *** To keep a local fully functional version of the application while developing
local-demo: build-local-demo up-local-demo

build-local-demo:
	@echo "Building images..."
	docker compose build db
	docker compose build server
	docker compose build data-view
	docker compose build workspace
	docker compose build admin

up-local-demo:
	@echo "Starting local demo instances..."
	docker compose up db server data-view workspace admin -d

# *** get test database ready
test: build-test-db up-test-db upgrade-test-db

build-test-db:
	docker compose build db-test

up-test-db: build-test-db
	docker compose up db-test -d --wait

upgrade-test-db: up-test-db
	@echo "Applying database migrations..."
	cd server && FLASK_APP=$(FLASK_APP) DATABASE_PORT=$(TEST_DATABASE_PORT) flask db upgrade
	@echo "Database migrations applied successfully."

# *** Development agent (boto-dev-agent), see docs/agentContainer.md
# *** Prefers podman when installed, falls back to docker.
CONTAINER_ENGINE := $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)

ifeq ($(CONTAINER_ENGINE),podman)
# *** Rootless podman maps container UIDs to host subuids; keep-id maps the host user 1:1.
agent: export USERNS_MODE := keep-id
# *** podman-compose (>= 1.1) applies keep-id natively; its default pod conflicts with it.
agent: export PODMAN_COMPOSE_PROVIDER := podman-compose
AGENT_COMPOSE_FLAGS := --in-pod false
else
# *** docker rejects podman's notmpcopyup and never copies into the mask anyway.
agent: export AGENT_SECRETS_TMPFS := ro
endif

# *** The container runs as the host user, so files the agent writes belong to it.
agent: export UID := $(shell id -u)
agent: export GID := $(shell id -g)

# *** Hides the secret files present now; `make agent` again after adding one.
AGENT_MASKS := .secrets/agent-masks.yml

agent:
	@{ test -f .secrets/agent.env && ls .secrets/*.private-key.pem >/dev/null 2>&1; } || \
		echo "No GitHub App credentials in .secrets/: the agent starts, but cannot push or open PRs (see docs/agentContainer.md)"
	@sh agent/secret-masks.sh > $(AGENT_MASKS)
	# Build (cached, so cheap when nothing changed) and start the agent detached
	$(CONTAINER_ENGINE) compose $(AGENT_COMPOSE_FLAGS) -f docker-compose.yml -f $(AGENT_MASKS) --profile agent up -d --build boto-dev-agent
	# Attach to it. Detach without stopping it with "ctrl + P + Q".
	$(CONTAINER_ENGINE) attach boto-dev-agent
