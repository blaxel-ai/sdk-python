ARGS:= $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

# Get git commit hash automatically
GIT_COMMIT := $(shell git rev-parse HEAD 2>/dev/null || echo "unknown")
GIT_COMMIT_SHORT := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

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

# Build with commit hash injection
build:
	@echo "🔨 Building Python SDK with commit: $(GIT_COMMIT_SHORT)"
	@echo "💉 Injecting commit hash into pyproject.toml"
	@if [ -f pyproject.toml ]; then \
		if grep -q "^\[tool\.blaxel\]" pyproject.toml; then \
			sed -i.bak 's/^commit = .*/commit = "$(GIT_COMMIT)"/' pyproject.toml && rm pyproject.toml.bak; \
		else \
			echo "" >> pyproject.toml; \
			echo "[tool.blaxel]" >> pyproject.toml; \
			echo 'commit = "$(GIT_COMMIT)"' >> pyproject.toml; \
		fi; \
	fi
	@echo "✅ Build completed with commit: $(GIT_COMMIT_SHORT)"

# Clean build artifacts and reset pyproject.toml
clean:
	@echo "🧹 Cleaning build artifacts"
	@git checkout pyproject.toml 2>/dev/null || true
	@rm -rf dist/ build/ *.egg-info/
	@echo "✅ Clean completed"

doc:
	rm -rf docs
	uv run pdoc blaxel src/* -o docs --force --skip-errors

lint:
	uv run ruff check --fix

tag:
	git checkout main
	git pull origin main
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
