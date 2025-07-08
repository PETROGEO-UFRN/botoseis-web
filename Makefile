# *** Makefile for building and managing Docker services

.PHONY: build-db build-server build-workspace build-data-view up-default \
				adm build-admin up-admin \
        build-test-db up-test-db upgrade-test-db \
        test

FLASK_APP := app.main
TEST_DATABASE_PORT := 5431

# *** Default targets, production like build (end user only, no admin module)
default: build-db server build-workspace build-data-view up-default

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
	docker compose up db workspace data-view -d

# *** Admin module and dependencies. 
adm: build-db build-server build-admin up-admin

build-admin:
	docker compose build admin

up-admin:
	@echo "Starting admin service and dependencies..."
	docker compose up db server admin -d

# *** Full demo in dedicated docker-stack
# *** To keep a local fully functional version of the application while developing
demo: build-demo up-demo

build-demo:
	docker compose build db
	docker build --tag boto/workspace:demo-1.0 ./workspace
	docker build --tag boto/data-view:demo-1.0 ./data-view
	docker build --tag boto/admin:demo-1.0 ./admin
# docker build --tag boto/server:demo-1.0 ./server

up-demo:
	docker compose -p boto-safe-demo up workspace data-view admin

# *** get test database ready
test: build-test-db up-test-db upgrade-test-db

build-test-db:
	docker compose build db-test

up-test-db: build-test-db
	docker compose up db-test

upgrade-test-db: up-test-db
	@echo "Applying database migrations..."
	cd server && FLASK_APP=$(FLASK_APP) DATABASE_PORT=$(TEST_DATABASE_PORT) flask db upgrade
	@echo "Database migrations applied successfully."
