.PHONY: help install dev test lint format check build run run-container clean install-mcp-client uninstall-mcp-client install-claude uninstall-claude

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Install with dev dependencies
	uv sync --extra dev

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .
	uv run ruff check --fix .

check: lint test ## Run all checks (lint + test)

run: ## Run MCP server locally (HTTP/SSE on port 8000)
	uv run fastmcp run src/mcp_server/server.py:mcp --transport sse --port 8000

run-dev: ## Run MCP server with auto-reload
	uv run fastmcp dev src/mcp_server/server.py:mcp --transport sse --port 8000

build: ## Build container image
	podman build -t mcp-template:latest .

run-container: ## Run container
	podman run --rm -p 8000:8000 mcp-template:latest

clean: ## Clean up build artifacts
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

install-mcp-client: ## Install to MCP client (set CLIENT=claude-code|continue|zed)
	@if [ -z "$(CLIENT)" ]; then \
		echo "Error: CLIENT variable not set"; \
		echo "Usage: make install-mcp-client CLIENT=claude-code"; \
		echo "Available clients: claude-code"; \
		exit 1; \
	fi
	@if [ ! -f "examples/integrations/$(CLIENT)/install.sh" ]; then \
		echo "Error: No install script for $(CLIENT)"; \
		echo "Available clients: claude-code"; \
		exit 1; \
	fi
	@bash examples/integrations/$(CLIENT)/install.sh

uninstall-mcp-client: ## Uninstall from MCP client (set CLIENT=claude-code|continue|zed)
	@if [ -z "$(CLIENT)" ]; then \
		echo "Error: CLIENT variable not set"; \
		echo "Usage: make uninstall-mcp-client CLIENT=claude-code"; \
		exit 1; \
	fi
	@if [ ! -f "examples/integrations/$(CLIENT)/uninstall.sh" ]; then \
		echo "Error: No uninstall script for $(CLIENT)"; \
		exit 1; \
	fi
	@bash examples/integrations/$(CLIENT)/uninstall.sh

install-claude: ## Install to Claude Code (convenience wrapper)
	@$(MAKE) install-mcp-client CLIENT=claude-code

uninstall-claude: ## Uninstall from Claude Code (convenience wrapper)
	@$(MAKE) uninstall-mcp-client CLIENT=claude-code

