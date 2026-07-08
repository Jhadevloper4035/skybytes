SHELL := /bin/sh

COMPOSE := docker compose
DEV_COMPOSE := $(COMPOSE) -f compose.yml -f compose.dev.yml
PROD_COMPOSE := $(COMPOSE)
DEPLOY_COMPOSE := $(COMPOSE) -f compose.production.yml
WEB := web

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "  make init-dev        Create .env from .env.development.example"
	@echo "  make init-prod       Create .env from .env.example"
	@echo ""
	@echo "  make dev-up         Start development stack in detached mode"
	@echo "  make dev            Start development stack in foreground"
	@echo "  make dev-build      Build and start development stack in detached mode"
	@echo "  make dev-down       Stop development stack"
	@echo "  make dev-logs       Follow development logs"
	@echo ""
	@echo "  make prod           Start production stack"
	@echo "  make prod-build     Build and start production stack"
	@echo "  make prod-pull      Pull Docker Hub image and start production stack"
	@echo "  make prod-down      Stop production stack"
	@echo "  make prod-logs      Follow production logs"
	@echo ""
	@echo "  make build          Build web image"
	@echo "  make compose-check  Validate Docker Compose config"
	@echo "  make ci             Run CI checks"
	@echo "  make check          Run Django system check"
	@echo "  make check-deploy   Run Django deployment check"
	@echo "  make migrate        Run migrations"
	@echo "  make collectstatic  Collect static files"
	@echo "  make shell          Open Django shell"
	@echo "  make bash           Open container shell"
	@echo "  make status         Show compose service status"
	@echo "  make clean          Stop stack and remove orphan containers"

.PHONY: init-dev
init-dev:
	@test -f .env || cp .env.development.example .env
	@echo ".env is ready for development"

.PHONY: init-prod
init-prod:
	@test -f .env || cp .env.example .env
	@echo ".env is ready; edit production secrets before deploying"

.PHONY: dev-up
dev-up:
	$(DEV_COMPOSE) up -d

.PHONY: dev
dev:
	$(DEV_COMPOSE) up

.PHONY: dev-build
dev-build:
	$(DEV_COMPOSE) up -d --build

.PHONY: dev-down
dev-down:
	$(DEV_COMPOSE) down

.PHONY: dev-logs
dev-logs:
	$(DEV_COMPOSE) logs -f

.PHONY: prod
prod:
	$(PROD_COMPOSE) up -d

.PHONY: prod-build
prod-build:
	$(PROD_COMPOSE) up -d --build

.PHONY: prod-pull
prod-pull:
	$(DEPLOY_COMPOSE) pull
	$(DEPLOY_COMPOSE) up -d

.PHONY: prod-down
prod-down:
	$(DEPLOY_COMPOSE) down

.PHONY: prod-logs
prod-logs:
	$(DEPLOY_COMPOSE) logs -f

.PHONY: build
build:
	$(PROD_COMPOSE) build $(WEB)

.PHONY: compose-check
compose-check:
	$(DEV_COMPOSE) config

.PHONY: ci
ci: init-dev compose-check build check

.PHONY: check
check:
	$(DEV_COMPOSE) run --rm --no-deps $(WEB) python manage.py check

.PHONY: check-deploy
check-deploy:
	$(PROD_COMPOSE) run --rm --no-deps $(WEB) python manage.py check --deploy

.PHONY: migrate
migrate:
	$(DEV_COMPOSE) run --rm $(WEB) python manage.py migrate

.PHONY: collectstatic
collectstatic:
	$(PROD_COMPOSE) run --rm $(WEB) python manage.py collectstatic --noinput

.PHONY: shell
shell:
	$(DEV_COMPOSE) run --rm $(WEB) python manage.py shell

.PHONY: bash
bash:
	$(DEV_COMPOSE) run --rm $(WEB) sh

.PHONY: status
status:
	$(DEPLOY_COMPOSE) ps

.PHONY: clean
clean:
	$(DEPLOY_COMPOSE) down --remove-orphans
