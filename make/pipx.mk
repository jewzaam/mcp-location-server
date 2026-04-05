.PHONY: pipx pipx-uninstall

# Distribution name from [project] name in pyproject.toml.
# May differ from PACKAGE_NAME (Python module) — e.g., my-tool vs my_tool.
PROJECT_NAME ?= mcp-location-server

pipx:  ## Install globally via pipx
	python3 -m pipx install .

pipx-uninstall:  ## Uninstall global pipx install
	python3 -m pipx uninstall $(PROJECT_NAME)
