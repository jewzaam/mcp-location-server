# MCP Location Server Makefile
# ==========================

# Variables
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
PYTHON := python3
UV := $(VENV_DIR)/bin/uv

# Colors for output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Default target
.DEFAULT_GOAL := help

# Help target - shows available commands
.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)MCP Location Server - Available Commands$(RESET)"
	@echo "========================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

# Create virtual environment
.PHONY: venv
venv: ## Create Python virtual environment
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
		printf "$(GREEN)✅ Virtual environment created$(RESET)\n"; \
	fi

# Install uv
.PHONY: uv
uv: venv ## Install uv
	@if [ ! -f "$(VENV_DIR)/bin/uv" ]; then \
		$(VENV_PYTHON) -m ensurepip --upgrade; \
		$(VENV_PYTHON) -m pip install uv; \
		printf "$(GREEN)✅ uv installed$(RESET)\n"; \
	fi


# Install requirements
.PHONY: requirements
requirements: uv ## Install package dependencies
	$(UV) pip install -r requirements.txt
	@printf "$(GREEN)✅ Dependencies installed$(RESET)\n"

# Install requirements
.PHONY: requirements-dev
requirements-dev: uv requirements ## Install package dependencies
	$(UV) pip install -r requirements-dev.txt
	@printf "$(GREEN)✅ Dev dependencies installed$(RESET)\n"

# Installation targets
.PHONY: install-mcp install-cursor

install-mcp: requirements ## Install the MCP Location server package
	$(UV) pip install -e .
	@printf "$(GREEN)✅ MCP Location server installed$(RESET)\n"

install-cursor: install-mcp ## Install MCP Location server for Cursor integration
	@$(VENV_PYTHON) scripts/update_cursor_config.py "$$(pwd)/$(VENV_PYTHON)" "$$(realpath .)"
	@printf "\n$(GREEN)Cursor MCP integration completed!$(RESET)\n"
	@printf "\n$(YELLOW)Next steps:$(RESET)\n"
	@printf "  1. Restart Cursor to load the new MCP server\n"
	@printf "  2. Open a new chat session (⌘+L on Mac, Ctrl+L on Linux)\n"
	@printf "  3. Look for 'location' in the MCP servers sidebar\n"
	@printf "  4. Test with: 'Find coordinates for Tokyo, Japan'\n"

# Run tests
.PHONY: test
test: requirements-dev ## Run all tests
	PYTHONPATH=src $(VENV_PYTHON) -m pytest tests/ -v
	@printf "$(GREEN)✅ Tests completed$(RESET)\n"

# Lint code
.PHONY: lint
lint: requirements-dev ## Run linting with ruff and mypy
	$(VENV_PYTHON) -m ruff check src/ tests/
	$(VENV_PYTHON) -m mypy src/
	@printf "$(GREEN)✅ Linting complete$(RESET)\n"

# Clean up
.PHONY: clean
clean: ## Clean up generated files
	rm -rf build/ dist/ *.egg-info/ src/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(VENV_DIR)
	@printf "$(GREEN)✅ Cleanup complete$(RESET)\n"
