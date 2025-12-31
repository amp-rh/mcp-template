# Development Setup

See @AGENTS.md for project-wide rules.

## Overview

Complete guide to setting up your development environment for MCP server development.

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Git

## Initial Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/YOUR-USERNAME/mcp-template.git
cd mcp-template

# Install dependencies (including dev dependencies)
uv sync --extra dev
```

## Running the Development Server

```bash
# Run with auto-reload (recommended for development)
make run-dev

# Or directly with uv
uv run fastmcp dev src/mcp_server/server.py:mcp --transport sse --port 8000

# Alternative: Run as a Python module
uv run python -m mcp_server
```

## Development Workflow

### 1. Format Code

```bash
make format
```

This runs:
- `ruff format .` - Auto-format code
- `ruff check --fix .` - Auto-fix linting issues

### 2. Run Linting

```bash
make lint
```

This checks code quality without making changes.

### 3. Run Type Checking

```bash
make typecheck
```

This runs mypy to verify type hints.

### 4. Run Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Generate HTML coverage report
make test-cov-html

# Run specific test file
uv run pytest tests/test_tools.py -v

# Run specific test
uv run pytest tests/test_tools.py::test_greet -v
```

### 5. Run All Checks

```bash
make check-all
```

This runs: format → lint → typecheck → test

## IDE Setup

### VS Code

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": false,
  "python.formatting.provider": "none",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "mypy.enabled": true,
  "mypy.runUsingActiveInterpreter": true
}
```

Install extensions:
- Ruff (charliermarsh.ruff)
- Mypy Type Checker

### PyCharm

1. Go to Settings → Project → Python Interpreter
2. Add interpreter → Add Local Interpreter → Existing environment
3. Select `.venv/bin/python`
4. Go to Settings → Tools → Ruff
5. Enable "Use ruff" and set path to `.venv/bin/ruff`
6. Enable "Format on save"

## Testing Patterns

### Async Tests

Use `@pytest.mark.asyncio` for async tests:

```python
import pytest

@pytest.mark.asyncio
async def test_async_tool():
    result = await my_async_tool("param")
    assert result == expected
```

### Test Structure

Tests mirror source structure:

```
src/mcp_server/tools/example_tools.py
tests/test_tools.py
```

## Container Development

```bash
# Build container
make build

# Run container
make run-container

# Or manually
podman build -t mcp-template:latest .
podman run --rm -p 8000:8000 mcp-template:latest
```

## Common Tasks

### Adding Dependencies

```bash
# Add production dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Sync dependencies
uv sync
```

### Running Python Module Directly

```bash
# Run as module
uv run python -m mcp_server

# This uses src/mcp_server/__main__.py as entry point
```

## Troubleshooting

### Import Errors

Ensure `src` is in PYTHONPATH:

```bash
export PYTHONPATH=src:$PYTHONPATH
```

Or use uv which handles this automatically.

### Type Errors

Run mypy to see detailed type errors:

```bash
make typecheck
```

### Test Failures

Run tests with verbose output:

```bash
uv run pytest -vv
```

## Pre-commit Hooks (Optional)

To enforce checks before commits:

```bash
# Install pre-commit
uv add --dev pre-commit

# Install hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

## Related

- @.agents/docs/tooling/uv.md - Package management
- @.agents/docs/tooling/pytest.md - Testing
- @.agents/docs/tooling/ruff.md - Linting and formatting
- @.agents/docs/workflows/testing.md - Testing workflow
