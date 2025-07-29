# MCP Location Server

A Model Context Protocol (MCP) server for geocoding addresses and coordinates using OpenStreetMap Nominatim API.

## Features

- **Forward geocoding**: Address/location → lat/long coordinates
- **Reverse geocoding**: Coordinates → address  
- **Free & open**: No API key required
- **Rate limited**: Respects 1 req/sec Nominatim policy

## Installation

```bash
# From project root with virtual environment activated
pip install -e ./mcp-location-server
```

## Cursor IDE Setup

### Prerequisites
- **Cursor IDE** (latest version)
- **Python 3.8+** with this MCP server installed
- **Node.js** (optional, for MCP Inspector testing)

### Step 1: Configure MCP in Cursor

The MCP configuration file is located at:
- **Linux**: `~/.cursor/mcp.json`  
- **macOS**: `~/Library/Application Support/Cursor/mcp.json`
- **Windows**: `%APPDATA%\Cursor\mcp.json`

### Step 2: Add Location Server Configuration

Add this to your `mcp.json` file:

```json
{
  "mcpServers": {
    "location": {
      "command": "/absolute/path/to/your/venv/bin/python",
      "args": ["-m", "mcp_location_server.server"],
      "cwd": "/absolute/path/to/mcp-location-server",
      "env": {
        "PYTHONPATH": "/absolute/path/to/your/venv/lib/python3.x/site-packages"
      }
    }
  }
}
```

**Important**: 
- Replace `/absolute/path/to/your/venv` with your actual virtual environment path
- Replace `/absolute/path/to/mcp-location-server` with your actual project path
- Update Python version in PYTHONPATH (`python3.x` → your version)

#### Alternative Configuration (System Python)
```json
{
  "mcpServers": {
    "location": {
      "command": "python3",
      "args": ["-m", "mcp_location_server.server"],
      "cwd": "/absolute/path/to/mcp-location-server"
    }
  }
}
```

### Step 3: Activate in Cursor

1. **Save** the `mcp.json` file
2. **Restart Cursor IDE** (required for config changes)
3. Go to **Settings** → **MCP**
4. Verify "location" server appears and is **enabled**
5. Click **Refresh** if server doesn't appear

### Step 4: Test Integration

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