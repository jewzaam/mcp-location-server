# Contributing to MCP Location Server

## Development Setup

1. Clone the repository
2. Run the setup using make: `make venv && make pip-install-test`

## Running Tests and Linting

The project uses make targets to ensure code quality:

```bash
make test    # Run tests
make lint    # Run all linting checks (ruff, mypy, black, isort)
```

## Pull Request Checks

This repository has automated PR checks that must pass before merging:

### Test Job
- Tests are run on Python 3.10, 3.11, and 3.12 using `make test`
- All tests must pass

### Lint Job
- **Ruff**: Code linting and style checks
- **MyPy**: Static type checking
- **Black**: Code formatting verification
- **isort**: Import sorting verification
- All checks run via `make lint`

## Making Changes

1. Create a feature branch from `main`
2. Make your changes
3. Run tests and linting locally: `make test && make lint`
4. Commit your changes
5. Push and create a pull request

The automated CI will run all checks on your PR using the same make targets. All checks must pass before the PR can be merged.

## Branch Protection

Once these PR checks are in place, branch protection can be enabled on the main branch requiring:
- PR reviews
- Status checks to pass
- Up-to-date branches before merging