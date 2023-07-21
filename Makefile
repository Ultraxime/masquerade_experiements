.PHONY: run build build_base compile measure full_compile silent full

full:
	./run.sh

silent:
	screen -d -m ./run.sh

full_compile: build
	docker compose -f docker-compose-compilation.yml run --remove-orphans full-compilation

run: kill measure compile

compile: build
	docker compose -f docker-compose-compilation.yml run --remove-orphans results-compilation

measure: build
	docker compose -f docker-compose-measure.yml run --remove-orphans bulk_download

build: build_base
	docker compose -f docker-compose-build.yml build

build_base:
	docker compose -f docker-compose-build.yml build dns

kill:
	docker ps | grep masquerade_experiements | wc -l
	RUNNING=$$(docker ps | grep masquerade_experiements | wc -l);\
	echo $$RUNNING ;\
	if [ $$RUNNING -ne 0 ]; then \
		docker kill $$(docker ps | grep masquerade_experiements | cut -d" " -f1) ; \
		sleep 10 ;\
		make kill ;\
	fi