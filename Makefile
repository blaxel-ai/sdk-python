ARGS:= $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

sdk-sandbox:
	cp ../sandbox/sandbox-api/docs/openapi.yml ./definition.yml
	rm -rf src/blaxel/sandbox/client/api src/blaxel/sandbox/client/models
	openapi-python-client generate \
		--path=definition.yml \
		--output-path=./tmp-sdk-sandbox \
		--overwrite \
		--custom-template-path=./templates \
		--config=./openapi-python-client.yml
	cp -r ./tmp-sdk-sandbox/blaxel/* ./src/blaxel/sandbox/client
	rm -rf ./tmp-sdk-sandbox
	uv run ruff check --fix

sdk-controlplane:
	cp ../controlplane/api/api/definitions/controlplane.yml ./definition.yml
	rm -rf src/blaxel/client/api src/blaxel/client/models
	openapi-python-client generate \
		--path=definition.yml \
		--output-path=./tmp-sdk-python \
		--overwrite \
		--custom-template-path=./templates \
		--config=./openapi-python-client.yml
	cp -r ./tmp-sdk-python/blaxel/* ./src/blaxel/client
	rm -rf ./tmp-sdk-python
	uv run ruff check --fix

sdk: sdk-sandbox sdk-controlplane

doc:
	rm -rf docs
	uv run pdoc blaxel-docs src/blaxel -o docs --force --skip-errors

lint:
	uv run ruff check --fix

tag:
	git tag -a v$(ARGS) -m "Release v$(ARGS)"
	git push origin v$(ARGS)

%:
	@:

.PHONY: sdk