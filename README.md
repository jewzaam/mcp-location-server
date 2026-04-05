# mcp-location-server

[![Test](https://github.com/jewzaam/mcp-location-server/actions/workflows/test.yml/badge.svg)](https://github.com/jewzaam/mcp-location-server/actions/workflows/test.yml) [![Coverage](https://github.com/jewzaam/mcp-location-server/actions/workflows/coverage.yml/badge.svg)](https://github.com/jewzaam/mcp-location-server/actions/workflows/coverage.yml) [![Lint](https://github.com/jewzaam/mcp-location-server/actions/workflows/lint.yml/badge.svg)](https://github.com/jewzaam/mcp-location-server/actions/workflows/lint.yml) [![Format](https://github.com/jewzaam/mcp-location-server/actions/workflows/format.yml/badge.svg)](https://github.com/jewzaam/mcp-location-server/actions/workflows/format.yml) [![Type Check](https://github.com/jewzaam/mcp-location-server/actions/workflows/typecheck.yml/badge.svg)](https://github.com/jewzaam/mcp-location-server/actions/workflows/typecheck.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Model Context Protocol (MCP) server for geocoding, reverse geocoding, and elevation lookup using free, open APIs.

## Overview

- **Forward geocoding**: Address/location to lat/long coordinates (via OpenStreetMap Nominatim)
- **Reverse geocoding**: Coordinates to address (via OpenStreetMap Nominatim)
- **Elevation lookup**: Coordinates to elevation in meters/feet (via Open Topo Data)
- **Free & open**: No API key required
- **Rate limited**: Respects 1 req/sec API usage policies

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended)

## Installation

```bash
git clone https://github.com/jewzaam/mcp-location-server.git
cd mcp-location-server
```

Install globally using either `uv` or `pipx` — both create an isolated venv so other pip operations can't break the install:

```bash
make install       # uses uv tool install
make pipx          # uses pipx install
```

For development (includes test/lint tooling):

```bash
make install-dev
```

## Configure Claude Code

**User-scoped** (available in all projects):

```bash
claude mcp add --scope user location -- mcp-location-server
```

Alternatively, use `uvx` so Claude Code resolves the tool fresh from the local source each invocation (most resilient to breakage):

```bash
claude mcp add --scope user location -- uvx --from /path/to/mcp-location-server mcp-location-server
```

**Project-scoped** (stored in `.mcp.json` in the project root):

```bash
claude mcp add --scope project location -- mcp-location-server
```

Verify the server is registered:

```bash
claude mcp list
```

## Configure Cursor IDE

Add to your Cursor MCP configuration (`~/.cursor/mcp.json` on Linux):

```json
{
  "mcpServers": {
    "location": {
      "command": "/absolute/path/to/mcp-location-server/.venv/bin/python",
      "args": ["-m", "mcp_location_server.server"],
      "cwd": "/absolute/path/to/mcp-location-server"
    }
  }
}
```

Or use the automated setup:

```bash
make install-cursor
```

After configuration, restart Cursor and enable the "location" server in Settings > MCP.

## Usage

### Available Tools

#### `geocode`

Convert address/location to coordinates:

```
"Find coordinates for Eiffel Tower"
"Get lat/long for 123 Main St, Boston, MA"
"Find up to 5 locations named 'Springfield'"
```

#### `reverse_geocode`

Convert coordinates to address:

```
"What's at coordinates 40.7128, -74.0060?"
"What address is at coordinates 48.8584, 2.2945?"
```

#### `get_elevation`

Get elevation data for coordinates:

```
"What's the elevation at 35.6894, -78.7767?"
"Get elevation for Mount Washington's coordinates"
```

## Development

```bash
make check       # Run format, lint, typecheck, test, coverage
make test        # Run tests only
make coverage    # Run tests with 80% coverage threshold
make format      # Format code with black
make lint        # Lint with flake8
make typecheck   # Type check with mypy
make help        # Show all available targets
```

## Limitations

- **Rate limiting**: 1 request/second maximum per API
- **Internet required**: Uses external Nominatim and Open Topo Data APIs
- **Coordinate precision**: APIs return nearest addressable location, not exact input coordinates

## Attribution

- **Nominatim API**: [nominatim.org](https://nominatim.org/) — OpenStreetMap data (c) OpenStreetMap contributors
- **Open Topo Data**: [opentopodata.org](https://www.opentopodata.org/) — elevation datasets (SRTM, ASTER, NED)
