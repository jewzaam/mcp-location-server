# MCP Location Server

A Model Context Protocol (MCP) server for geocoding addresses and coordinates using OpenStreetMap Nominatim API.

## Features

- **Forward geocoding**: Address/location → lat/long coordinates
- **Reverse geocoding**: Coordinates → address  
- **Free & open**: No API key required
- **Rate limited**: Respects 1 req/sec Nominatim policy

## Installation

### Quick Install (Recommended)

```bash
# Complete install: MCP server + Cursor configuration
make install
```

Or install components separately:

```bash
# Install MCP server only
make install-mcp

# Configure Cursor IDE (after MCP server is installed)
make install-cursor
```

This will:
- Create a Python virtual environment
- Install the package in development mode
- Generate Cursor IDE configuration

### Manual Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install package
pip install -e .
```

### Available Make Commands

Run `make help` to see all available commands:

```bash
make help                    # Show all available commands
make install                 # Complete install: MCP server + Cursor configuration
make install-mcp             # Install MCP server only
make install-cursor          # Configure Cursor IDE integration
make install-dev             # Install with development dependencies
make test                    # Run all tests
make test-server             # Run comprehensive server tests
make dev                     # Start server in development mode
make format                  # Format code with black and isort
make lint                    # Run linting with ruff and mypy
make check                   # Run linting and tests
make clean                   # Clean up generated files
make doctor                  # Check if everything is working
make status                  # Show project status
```

## Cursor IDE Setup

### Prerequisites
- **Cursor IDE** (latest version)
- **Python 3.8+** with this MCP server installed (use `make install`)
- **Node.js** (optional, for MCP Inspector testing)

### Easy Setup with Makefile

**Option 1: Complete Setup (Recommended)**
```bash
make install
```
This installs the MCP server and shows Cursor configuration in one step.

**Option 2: Separate Steps**
```bash
# Step 1: Install MCP server
make install-mcp

# Step 2: Configure Cursor IDE
make install-cursor
```

**After either option:**
1. **Copy the generated JSON** to your MCP configuration file:
   - **Linux**: `~/.cursor/mcp.json`  
   - **macOS**: `~/Library/Application Support/Cursor/mcp.json`
   - **Windows**: `%APPDATA%\Cursor\mcp.json`

2. **Restart Cursor IDE** completely

3. **Enable the server**: Go to **Settings** → **MCP** and enable the "location" server

### Manual Configuration

If you prefer manual setup, add this to your `mcp.json` file:

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

**Important**: Replace `/absolute/path/to/mcp-location-server` with your actual project path.

### Test Integration

In Cursor's AI panel (`Ctrl+L` or `Cmd+L`), switch to Agent mode (`Ctrl+.`) and test with the examples below.

## Available Tools & Examples

### `geocode`
Convert address/location to coordinates:
```
"Find coordinates for Eiffel Tower"
"Get lat/long for 123 Main St, Boston, MA" 
"Get coordinates for the Empire State Building"
"Find up to 5 locations named 'Springfield'"
```

### `reverse_geocode`  
Convert coordinates to address:
```
"What's at coordinates 40.7128, -74.0060?"
"What address is at coordinates 48.8584, 2.2945?"
```

## Troubleshooting

### Server Not Appearing
- Check `mcp.json` file location and JSON syntax
- Verify all file paths are absolute and accessible
- Restart Cursor completely

### Server Shows "Disconnected/Error"
Test the command manually:
```bash
/absolute/path/to/venv/bin/python -m mcp_location_server.server
```

### Tools Not Available in Agent Mode
- Confirm server is active in MCP settings
- Try explicit requests: "Use the geocode tool to find..."
- Check Cursor's output panel for error messages

### Debug Mode
Add to your server configuration:
```json
{
  "mcpServers": {
    "location": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["-m", "mcp_location_server.server", "--verbose"],
      "cwd": "/absolute/path/to/mcp-location-server",
      "env": {
        "PYTHONPATH": "/absolute/path/to/venv/lib/python3.x/site-packages",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## Limitations

- **Coordinate precision**: API returns nearest addressable location, not exact input coordinates
- **Rate limiting**: 1 request/second maximum
- **Requires restart**: Cursor needs full restart for MCP config changes
- **Internet required**: Uses external Nominatim API

## Testing

```bash
# Direct test
python test_client.py

# MCP Inspector (requires Node.js)
npx @modelcontextprotocol/inspector
```

## Attribution

- **Nominatim API**: Used under Apache 2.0 license - [Nominatim](https://nominatim.org/)
- **Geocoding data**: Provided by Nominatim using OpenStreetMap data © OpenStreetMap contributors 