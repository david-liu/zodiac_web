#!/bin/bash
#
#
# If the first argument is "run"...

init:
	./scripts/install_env

doc:
	apidoc -i src/ -o {app_name}_api_doc/

docker-build:
	./scripts/build_docker

docker-run-it:
	docker run -it -p {port}:{port}  zodiac_web/{app_name}

docker-run:
	docker run -d -p {port}:{port}  zodiac_web/{app_name}