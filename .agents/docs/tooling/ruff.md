# Linting and Formatting with Ruff

See @AGENTS.md for project-wide rules.

## Overview

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

## Commands

```bash
# Check for issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

## Configuration

Configuration is in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "N",      # pep8-naming
    "S",      # flake8-bandit (security)
    "BLE",    # flake8-blind-except
    "A",      # flake8-builtins
    "C90",    # mccabe complexity
    "DTZ",    # flake8-datetimez
    "EM",     # flake8-errmsg
    "PIE",    # flake8-pie
    "PT",     # flake8-pytest-style
    "RSE",    # flake8-raise
    "RET",    # flake8-return
    "SIM",    # flake8-simplify
    "ARG",    # flake8-unused-arguments
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented-out code)
    "PL",     # Pylint
    "TRY",    # tryceratops
    "PERF",   # Perflint
    "RUF",    # Ruff-specific rules
]

ignore = [
    "S101",   # Use of assert (needed for pytest)
    "COM812", # Trailing comma (conflicts with formatter)
    "ISC001", # Implicit string concatenation (conflicts with formatter)
    "T201",   # print found (useful for debugging)
]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-args = 5
max-branches = 12
```

## Enabled Rule Categories

### Core Linting
- **E/W**: PEP 8 errors and warnings
- **F**: Pyflakes (unused imports, undefined names)
- **I**: Import sorting (isort)

### Code Quality
- **B**: Bugbear (common bugs and design problems)
- **C4**: Comprehensions (list/dict/set improvements)
- **UP**: Pyupgrade (modern Python syntax)
- **N**: PEP 8 naming conventions
- **C90**: McCabe complexity (max 10)

### Security & Safety
- **S**: Bandit security checks
- **BLE**: Blind except (catch specific exceptions)
- **A**: Shadowing built-ins

### Best Practices
- **SIM**: Simplification suggestions
- **PIE**: Miscellaneous improvements
- **RET**: Return statement improvements
- **ARG**: Unused argument detection
- **PTH**: Use pathlib instead of os.path
- **ERA**: Detect commented-out code

### Python Patterns
- **EM**: Error message best practices
- **TRY**: Exception handling patterns
- **RSE**: Unnecessary exception raises
- **DTZ**: Timezone-aware datetime usage

### Testing
- **PT**: Pytest style and best practices

### Performance
- **PERF**: Performance anti-patterns

## Rules

- MUST run `ruff check .` before committing
- MUST fix all linting errors before committing
- SHOULD run `ruff format .` to maintain consistent style

## Common Issues

### Import Sorting (I001)
Imports not sorted correctly. Fix with `ruff check --fix .`

### Unused Imports (F401)
Remove unused imports or add `# noqa: F401` if re-exporting.

### Line Too Long (E501)
Break long lines. Max line length is 88 characters.

