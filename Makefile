ARGS:= $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

install:
	uv sync --all-groups --all-packages --all-extras

install-groups:
	uv sync --refresh --force-reinstall --extra telemetry --extra langgraph

sdk-sandbox:
	@echo "Downloading sandbox definition from blaxel-ai/sandbox"
	@curl -H "Authorization: token $$(gh auth token)" \
		-H "Accept: application/vnd.github.v3.raw" \
		-o ./definition.yml \
		https://api.github.com/repos/blaxel-ai/sandbox/contents/sandbox-api/docs/openapi.yml?ref=main
	rm -rf src/blaxel/core/sandbox/client/api src/blaxel/core/sandbox/client/models
	openapi-python-client generate \
		--path=definition.yml \
		--output-path=./tmp-sdk-sandbox \
		--overwrite \
		--custom-template-path=./templates \
		--config=./openapi-python-client.yml
	cp -r ./tmp-sdk-sandbox/blaxel/* ./src/blaxel/core/sandbox/client
	rm -rf ./tmp-sdk-sandbox
	uv run ruff check --fix

sdk-controlplane:
	@echo "Downloading controlplane definition from blaxel-ai/controlplane"
	@curl -H "Authorization: token $$(gh auth token)" \
		-H "Accept: application/vnd.github.v3.raw" \
		-o ./definition.yml \
		https://api.github.com/repos/blaxel-ai/controlplane/contents/api/api/definitions/controlplane.yml?ref=main
	rm -rf src/blaxel/core/client/api src/blaxel/core/client/models
	openapi-python-client generate \
		--path=definition.yml \
		--output-path=./tmp-sdk-python \
		--overwrite \
		--custom-template-path=./templates \
		--config=./openapi-python-client.yml
	cp -r ./tmp-sdk-python/blaxel/* ./src/blaxel/core/client
	rm -rf ./tmp-sdk-python
	uv run ruff check --fix

sdk: sdk-sandbox sdk-controlplane

doc:
	rm -rf docs
	uv run pdoc blaxel src/* -o docs --force --skip-errors

lint:
	uv run ruff check --fix

tag:
	git tag -a v$(ARGS) -m "Release v$(ARGS)"
	git push origin v$(ARGS)

test: install-dev
	uv run pytest tests/ -v

test-with-telemetry:
	uv sync --group test --extra telemetry
	pip install -e .
	uv run pytest tests/ -v

install-dev:
	uv sync --group test
	pip install -e .

%:
	@:

.PHONY: sdk
