# MCP Location Server Requirements

## Core Functional Requirements

- Provide lat/long coordinates for given addresses or general locations like cities
- Use an open API (no API key requirements)
- Support both forward geocoding (address → coordinates) and reverse geocoding (coordinates → address)
- Implement proper rate limiting to respect API usage policies
- Include robust error handling for invalid addresses and API failures

## Technical Requirements

### MCP Server Standards
- Use stdio transport only for local MCP server deployment
- Follow underscore naming convention for module structure
- Implement standard MCP protocol for tool discovery and execution

### API Integration
- Use OpenStreetMap Nominatim API (free, no API key required)
- Implement 1 request/second rate limiting to respect Nominatim usage policy
- Handle network failures and API timeouts gracefully
- Return structured data with proper coordinates and location metadata

### Tools Specification
- `geocode`: Convert address/location to lat/long coordinates
  - Input: address string, optional result limit
  - Output: structured results with coordinates, location names, and metadata
- `reverse_geocode`: Convert coordinates to address
  - Input: latitude and longitude values
  - Output: structured address information

### Client Integration
- Cursor IDE compatibility with stdio transport
- Support for natural language queries through MCP client interface
- Proper tool documentation for client discovery

## Data Handling

### Input Processing
- Accept various address formats (street addresses, cities, landmarks, POIs)
- Validate coordinate inputs for reverse geocoding
- Handle multiple result scenarios for ambiguous queries

### Output Format
- Provide consistent structured responses
- Include confidence/importance scores when available
- Return human-readable location names and precise coordinates
- Handle cases where no results are found

### API Behavior
- Document coordinate precision limitations (API returns nearest addressable location)
- Maintain attribution requirements for data sources
- Respect external service usage policies and rate limits

## Installation & Testing

### Setup Requirements
- Python 3.8+ compatibility
- Standard Python packaging with pyproject.toml
- Development dependencies for testing and code quality

### Testing Coverage
- Unit tests for geocoding service functionality
- Integration tests with live API calls
- Error scenario testing for network failures and invalid inputs
- MCP protocol compliance testing

### Documentation
- Self-contained setup instructions
- Cursor integration guide with troubleshooting
- Usage examples for both geocoding tools
- API limitations and attribution requirements 