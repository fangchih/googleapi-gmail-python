DOCKER_IMAGE = my-googlecloud-sdk:python-gmail
AUTH_VOLUME = my-python-gmail-auth
DOCKER_RUN_CMD = --rm --volumes-from ${AUTH_VOLUME} -w /app -v ${CURDIR}:/app -v ${GOOGLE_APPLICATION_CREDENTIALS}:/key/credentials.json
ENV_INIT_CMD = gcloud auth login

container:
	@if [ "$$(docker ps -a | grep ${AUTH_VOLUME})" == "" ]; then \
		docker build -f Dockerfile . -t ${DOCKER_IMAGE} && \
	  docker run -ti --name ${AUTH_VOLUME} ${DOCKER_IMAGE} ${ENV_INIT_CMD}; \
	fi

checkenv:
ifndef GOOGLE_APPLICATION_CREDENTIALS
	$(error GOOGLE_APPLICATION_CREDENTIALS is undefined)
endif

bash: container checkenv
	docker run -ti ${DOCKER_RUN_CMD} ${DOCKER_IMAGE} /bin/bash

listlabels: container checkenv
	docker run ${DOCKER_RUN_CMD} ${DOCKER_IMAGE} python3 src/listlabels.py

watch: container checkenv
	docker run ${DOCKER_RUN_CMD} ${DOCKER_IMAGE} python3 src/watch.py

.PHONY: container bash listlabels checkenv