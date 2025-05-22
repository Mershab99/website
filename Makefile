# Variables
docker_registry ?= $(CI_REGISTRY)
image_name ?= $(CI_REGISTRY_IMAGE)
image_tag ?= $(CI_COMMIT_REF_SLUG)
#platforms ?= linux/amd64,linux/arm64
platforms ?= linux/amd64
full_image_name := $(image_name):$(image_tag)

# Targets
.PHONY: docker build push

build-local:
	docker buildx build --platform $(platforms) -t $(full_image_name) --load .
docker:
	docker buildx create --use --name multiarch-builder || true
	docker login -u "$(CI_REGISTRY_USER)" -p "$(CI_REGISTRY_PASSWORD)" $(docker_registry)
	docker buildx build --platform $(platforms) -t "$(full_image_name)" --push .

build-helm:
	helm dep update ./charts/website
