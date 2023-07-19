.PHONY: run build build_base

full:
	./run.sh

silent:
	screen -d -m ./run.sh

full_compile: build
	docker compose -f docker-compose-compilation.yml run --remove-orphans full-compilation

run: measure compile

compile: build
	docker compose -f docker-compose-compilation.yml run --remove-orphans results-compilation

measure: build
	docker compose -f docker-compose-measure.yml run --remove-orphans bulk_download

build: build_base
	docker compose -f docker-compose-build.yml build

build_base:
	docker compose -f docker-compose-build.yml build dns
