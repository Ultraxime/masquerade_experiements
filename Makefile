# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:05:37
#
# This file is part of Masquerade experiements.
#
# Masquerade experiements is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later version.
#
# Masquerade experiements is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Masquerade experiements. If not, see <https://www.gnu.org/licenses/>.

.PHONY: run build build_base compile measure full_compile silent full

full:
	./run.sh

silent:
	screen -d -m ./run.sh

full_compile: build
	docker compose -f docker-compose-compilation.yml run --remove-orphans --rm full-compilation

run: kill results measure compile

compile: build
	docker compose -f docker-compose-compilation.yml run --remove-orphans --rm results-compilation

measure: build
	docker compose -f docker-compose-measure.yml run --remove-orphans --rm bulk_download

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

clean: kill
	docker container prune -f && docker image prune -f && docker volume prune -f && docker network prune -f

push: build
	docker compose -f docker-compose-build.yml push

pull:
	docker compose -f docker-compose-build.yml pull

results:
	mkdir -p results
