SHELL := /bin/sh

COMPOSE := docker compose
DEV_COMPOSE := $(COMPOSE) -f compose.dev.yml
PROD_COMPOSE := $(COMPOSE) -f compose.production.yml
WEB := web
LOCAL_WEB_IMAGE ?= skybyte-web:local
SSL_EMAIL ?= info@skybytedevelopers.com
SSL_DOMAINS := -d skybytedevelopers.com -d www.skybytedevelopers.com
CERTBOT_IMAGE ?= certbot/certbot:latest

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "  make dev-up         Start development stack in detached mode"
	@echo "  make dev            Start development stack in foreground"
	@echo "  make dev-build      Build and start development stack in detached mode"
	@echo "  make dev-down       Stop development stack"
	@echo "  make dev-logs       Follow development logs"
	@echo ""
	@echo "  make prod           Start production stack"
	@echo "  make prod-build     Build and start production stack"
	@echo "  make prod-pull      Pull fresh images, recreate production stack, and prune old containers/images"
	@echo "  make prod-down      Stop production stack"
	@echo "  make prod-logs      Follow production logs"
	@echo "  make ssl-init       Generate first Let's Encrypt SSL certificate"
	@echo "  make ssl-renew      Renew SSL certificate and reload nginx"
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
	docker build -t $(LOCAL_WEB_IMAGE) .
	WEB_IMAGE=$(LOCAL_WEB_IMAGE) $(PROD_COMPOSE) up -d

.PHONY: prod-pull
prod-pull:
	$(PROD_COMPOSE) down --remove-orphans
	$(PROD_COMPOSE) pull
	$(PROD_COMPOSE) up -d --force-recreate --remove-orphans
	docker container prune -f
	docker image prune -af

.PHONY: prod-down
prod-down:
	$(PROD_COMPOSE) down

.PHONY: prod-logs
prod-logs:
	$(PROD_COMPOSE) logs -f

.PHONY: ssl-init
ssl-init:
	mkdir -p /var/www/certbot /etc/letsencrypt
	$(PROD_COMPOSE) stop nginx || true
	docker run --rm -p 80:80 -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot:/var/www/certbot $(CERTBOT_IMAGE) certonly --standalone --non-interactive --agree-tos --email $(SSL_EMAIL) $(SSL_DOMAINS)
	$(PROD_COMPOSE) up -d nginx

.PHONY: ssl-renew
ssl-renew:
	mkdir -p /var/www/certbot /etc/letsencrypt
	docker run --rm -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot:/var/www/certbot $(CERTBOT_IMAGE) renew --webroot -w /var/www/certbot
	$(PROD_COMPOSE) exec nginx nginx -s reload

.PHONY: build
build:
	docker build -t $(LOCAL_WEB_IMAGE) .

.PHONY: compose-check
compose-check:
	$(DEV_COMPOSE) config

.PHONY: ci
ci: compose-check build check

.PHONY: check
check:
	$(DEV_COMPOSE) run --rm --no-deps $(WEB) python manage.py check

.PHONY: check-deploy
check-deploy:
	WEB_IMAGE=$(LOCAL_WEB_IMAGE) $(PROD_COMPOSE) run --rm --no-deps $(WEB) python manage.py check --deploy

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
	$(PROD_COMPOSE) ps

.PHONY: clean
clean:
	$(PROD_COMPOSE) down --remove-orphans
