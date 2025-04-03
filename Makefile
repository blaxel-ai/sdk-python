ARGS:= $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

sdk:
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