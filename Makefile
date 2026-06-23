SHELL := /bin/bash

COMPOSE ?= docker compose
DOCKER_CONFIG ?= $(HOME)/.docker
SUDO ?= sudo -E

.PHONY: up down restart logs ps build test lint migrate shell

up:
	DOCKER_CONFIG="$(DOCKER_CONFIG)" $(SUDO) $(COMPOSE) up -d --build

down:
	DOCKER_CONFIG="$(DOCKER_CONFIG)" $(SUDO) $(COMPOSE) down

restart: down up

logs:
	DOCKER_CONFIG="$(DOCKER_CONFIG)" $(SUDO) $(COMPOSE) logs -f

ps:
	DOCKER_CONFIG="$(DOCKER_CONFIG)" $(SUDO) $(COMPOSE) ps

build:
	DOCKER_CONFIG="$(DOCKER_CONFIG)" $(SUDO) $(COMPOSE) build

test:
	. .venv/bin/activate && pytest -p no:cov -q

lint:
	. .venv/bin/activate && ruff check .

migrate:
	. .venv/bin/activate && python manage.py migrate --noinput

shell:
	. .venv/bin/activate && python manage.py shell
