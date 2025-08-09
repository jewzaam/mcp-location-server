# MCP Location Server Makefile
# ==========================

# Variables
PYTHON := python3
UV := uv
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python

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
		printf "$(BLUE)Creating virtual environment...$(RESET)\n"; \
		$(UV) venv $(VENV_DIR); \
		printf "$(GREEN)✅ Virtual environment created$(RESET)\n"; \
	else \
		printf "$(YELLOW)Virtual environment already exists$(RESET)\n"; \
	fi

# Install uv
.PHONY: uv
uv:
	@if [ ! -f "$(VENV_DIR)/bin/uv" ]; then \
		printf "$(BLUE)Installing uv...$(RESET)\n"; \
		$(VENV_PYTHON) -m ensurepip --upgrade; \
		$(VENV_PYTHON) -m pip install uv; \
		printf "$(GREEN)✅ uv installed$(RESET)\n"; \
	fi

# Install requirements
.PHONY: pip-install-test
pip-install-test: uv venv ## Install package dependencies
	@printf "$(BLUE)Installing dependencies...$(RESET)\n"
	$(UV) pip install -r requirements-test.txt
	@printf "$(GREEN)✅ Dependencies installed$(RESET)\n"

# Installation targets
.PHONY: install-mcp install-cursor

install-mcp: pip-install-test ## Install the MCP Location server package
	@printf "$(BLUE)Installing MCP Location Server package...$(RESET)\n"
	@printf "$(GREEN)MCP Location Server package installed successfully!$(RESET)\n"
	@printf "\n"
	@printf "$(CYAN)The server can now be run with:$(RESET)\n"
	@printf "  mcp-location-server\n"
	@printf "  or\n"
	@printf "  python -m mcp_location_server.server\n"

install-cursor: install-mcp ## Install MCP Location server for Cursor integration
	@printf "$(BLUE)Setting up MCP Location Server for Cursor...$(RESET)\n"
	@printf "$(YELLOW)Creating Cursor configuration...$(RESET)\n"
	@if [ ! -d "$$HOME/.cursor" ]; then \
		printf "$(RED)Error: Cursor directory ($$HOME/.cursor) not found!$(RESET)\n"; \
		printf "$(YELLOW)Please install Cursor first or create the directory manually$(RESET)\n"; \
		exit 1; \
	fi
	@printf "$(YELLOW)Updating Cursor MCP configuration...$(RESET)\n"
	@$(VENV_PYTHON) scripts/update_cursor_config.py "$$(pwd)/$(VENV_PYTHON)" "$$(realpath .)"
	@printf "\n$(GREEN)Cursor MCP integration completed!$(RESET)\n"
	@printf "\n$(YELLOW)Next steps:$(RESET)\n"
	@printf "  1. Restart Cursor to load the new MCP server\n"
	@printf "  2. Open a new chat session (⌘+L on Mac, Ctrl+L on Linux)\n"
	@printf "  3. Look for 'location' in the MCP servers sidebar\n"
	@printf "  4. Test with: 'Find coordinates for Tokyo, Japan'\n"

# Run tests
.PHONY: test
test: venv pip-install-test ## Run all tests
	@printf "$(BLUE)Running tests...$(RESET)\n"
	$(VENV_PYTHON) -m pytest tests/ -v
	@printf "$(GREEN)✅ Tests completed$(RESET)\n"

# Lint code
.PHONY: lint
lint: venv pip-install-test ## Run linting with ruff and mypy
	@printf "$(BLUE)Running linters...$(RESET)\n"
	$(VENV_PYTHON) -m ruff check src/ tests/
	$(VENV_PYTHON) -m mypy src/
	@printf "$(GREEN)✅ Linting complete$(RESET)\n"

# Clean up
.PHONY: clean
clean: ## Clean up generated files
	@printf "$(BLUE)Cleaning up...$(RESET)\n"
	rm -rf build/ dist/ *.egg-info/ src/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(VENV_DIR)
	@printf "$(GREEN)✅ Cleanup complete$(RESET)\n"
