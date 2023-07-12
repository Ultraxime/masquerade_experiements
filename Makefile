.PHONY: run build build_base

run: build docker-compose.yml
	docker compose --profile run up

build: build_base docker-compose.yml
	docker compose --profile run build

build_base: docker-compose.yml
	docker compose --profile build build
