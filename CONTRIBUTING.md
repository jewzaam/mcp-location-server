# Contributing to MCP Location Server

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
4. Install development dependencies: `pip install -r requirements-test.txt`
5. Install the package in development mode: `pip install -e .`

## Running Tests and Linting

The project uses several tools to ensure code quality:

### Using Make (Recommended)
```bash
make test    # Run tests
make lint    # Run all linting checks
```

### Manual Commands
```bash
# Run tests
python -m pytest tests/ -v

# Run linting
python -m ruff check src/
python -m ruff check tests/ --ignore=SLF001  # Ignore private member access in tests
python -m mypy src/

# Check code formatting
python -m black --check src/ tests/
python -m isort --check-only src/ tests/

# Auto-fix formatting
python -m black src/ tests/
python -m isort src/ tests/
```

## Pull Request Checks

This repository has automated PR checks that must pass before merging:

### Test Job
- Tests are run on Python 3.10, 3.11, and 3.12
- All tests must pass (currently 26/29 tests pass - 3 have regex pattern issues)

### Lint Job
- **Ruff**: Code linting and style checks
- **MyPy**: Static type checking
- **Black**: Code formatting verification
- **isort**: Import sorting verification

## Making Changes

1. Create a feature branch from `main`
2. Make your changes
3. Run tests and linting locally: `make test && make lint`
4. Fix any formatting issues: `python -m black src/ tests/ && python -m isort src/ tests/`
5. Commit your changes
6. Push and create a pull request

The automated CI will run all checks on your PR. All checks must pass before the PR can be merged.

## Branch Protection

Once these PR checks are in place, branch protection can be enabled on the main branch requiring:
- PR reviews
- Status checks to pass
- Up-to-date branches before merging