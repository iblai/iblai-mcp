# MCP Creator

A tool to generate MCP (Model Context Protocol) servers from HAR (HTTP Archive) files.

## Overview

MCP Creator analyzes HAR files captured from browser network activity or API testing tools to automatically generate comprehensive MCP servers. This enables rapid creation of MCP servers for any API service.

## Features

- **HAR File Parsing**: Extracts API endpoints, request/response patterns, and authentication mechanisms
- **Smart Endpoint Detection**: Filters out static assets and identifies API calls
- **Path Parameter Extraction**: Automatically detects UUIDs, numeric IDs, and other path parameters
- **Query Parameter Discovery**: Extracts and documents query parameters with examples
- **Multiple Authentication Methods**:
  - API Key authentication
  - Bearer token authentication
  - Basic authentication
  - Custom header authentication
  - OAuth2 client credentials flow
- **Production-Ready Code**: Generates well-structured, documented Python MCP servers

## Installation

```bash
cd mcp-creator
pip install -e .
```

Or just use directly with Python:

```bash
python cli.py <har_file>
```

## Usage

### Analyze a HAR File

See what endpoints and authentication patterns were discovered:

```bash
python cli.py analyze your-api.har
```

Output includes:
- Service name (auto-detected from URLs)
- Base URL
- Authentication patterns found
- List of endpoints with parameters

### Generate an MCP Server

Create a complete MCP server from a HAR file:

```bash
# Auto-detect name from HAR file
python cli.py create your-api.har

# Specify custom name
python cli.py create your-api.har --name myservice

# Specify output directory
python cli.py create your-api.har --output ./servers
```

### Quick Usage

```bash
# Shortcut - same as 'create'
python cli.py your-api.har

# Analyze only
python cli.py your-api.har --analyze
```

## How to Capture HAR Files

### Chrome/Brave/Edge

1. Open Developer Tools (F12)
2. Go to the Network tab
3. Perform the API operations you want to capture
4. Right-click on the network requests list
5. Select "Save all as HAR with content"

### Firefox

1. Open Developer Tools (F12)
2. Go to the Network tab
3. Perform the API operations
4. Click the gear icon and select "Save All As HAR"

### Postman

1. Make your API requests
2. Click on the History tab
3. Select the requests you want to export
4. Right-click and select "Export" > "HAR"

## Generated Server Structure

```
iblai-<service>/
├── pyproject.toml          # Project configuration
├── README.md               # Documentation
├── .env.example            # Environment variables template
└── iblai_<service>/
    ├── __init__.py
    ├── server.py           # Main MCP server
    ├── auth.py             # Authentication manager
    └── client.py           # HTTP client
```

## Authentication Configuration

The generated servers support multiple authentication methods via environment variables:

### API Key

```bash
export SERVICENAME_AUTH_TYPE=api_key
export SERVICENAME_API_KEY=your_api_key
export SERVICENAME_API_KEY_HEADER=X-API-Key  # optional, default: X-API-Key
```

### Bearer Token

```bash
export SERVICENAME_AUTH_TYPE=bearer
export SERVICENAME_BEARER_TOKEN=your_token
```

### Basic Auth

```bash
export SERVICENAME_AUTH_TYPE=basic
export SERVICENAME_BASIC_USERNAME=your_username
export SERVICENAME_BASIC_PASSWORD=your_password
```

### OAuth2 Client Credentials

```bash
export SERVICENAME_AUTH_TYPE=oauth2_client_credentials
export SERVICENAME_OAUTH2_CLIENT_ID=your_client_id
export SERVICENAME_OAUTH2_CLIENT_SECRET=your_client_secret
export SERVICENAME_OAUTH2_TOKEN_URL=https://auth.example.com/oauth/token
export SERVICENAME_OAUTH2_SCOPE=read write  # optional
```

## Best Practices for HAR Capture

1. **Clear existing requests**: Start with a clean Network tab
2. **Preserve log**: Enable "Preserve log" to keep requests across page navigations
3. **Include all variations**: Perform different operations to capture all endpoints
4. **Multiple parameters**: Try different query parameters to capture all options
5. **Authenticated sessions**: Capture while logged in to see auth headers

## Naming Convention

All generated servers follow the naming convention: `iblai-<service>`

The service name is auto-detected from the HAR file's URLs, but can be overridden with `--name`.

## Extending Generated Servers

The generated servers are meant to be starting points. Common extensions:

1. **Add custom tools**: Edit `server.py` to add tools not in the HAR
2. **Add resources**: Expose data as MCP resources
3. **Add prompts**: Create prompt templates
4. **Enhanced error handling**: Customize error responses
5. **Rate limiting**: Add rate limiting to the client

## License

MIT
