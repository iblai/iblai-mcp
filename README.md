# iblai-mcp

A collection of MCP (Model Context Protocol) servers for various APIs, along with a tool to generate new MCP servers from HAR files.

## Quick Start

### Using an Existing MCP Server

#### Local Installation

```bash
# Clone the repository
git clone https://github.com/iblai/iblai-mcp.git
cd iblai-mcp

# Install and run an MCP server (e.g., iblai-blog)
cd iblai-blog
uv sync
uv run iblai-blog
```

#### Connect from Claude Desktop

Add to your Claude Desktop configuration:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "iblai-blog": {
      "command": "uv",
      "args": ["run", "iblai-blog"],
      "cwd": "/path/to/iblai-mcp/iblai-blog"
    }
  }
}
```

#### Connect from Claude Code

```bash
claude mcp add iblai-blog -- uv run --directory /path/to/iblai-mcp/iblai-blog iblai-blog
```

#### Connect to a Remote MCP Server

If an MCP server is hosted remotely:

**Claude Desktop:**
```json
{
  "mcpServers": {
    "iblai-blog": {
      "url": "https://your-server.com/iblai-blog/sse"
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add iblai-blog --transport sse https://your-server.com/iblai-blog/sse
```

## Available MCP Servers

| Server | Description | Base URL |
|--------|-------------|----------|
| [iblai-blog](./iblai-blog) | Blog API for IBL.ai | https://blog.ibl.ai |

## Creating New MCP Servers

Use the MCP Creator tool to generate new MCP servers from HAR files captured from browser network activity.

### Step 1: Capture a HAR File

1. Open your browser's Developer Tools (F12)
2. Go to the **Network** tab
3. Perform the API operations you want to capture
4. Right-click on the network requests list
5. Select **Save all as HAR with content**

### Step 2: Analyze the HAR File

See what endpoints and authentication patterns were discovered:

```bash
python mcp-creator/cli.py analyze your-api.har
```

Example output:
```
============================================================
HAR Analysis: your-api.har
============================================================

Service Name: example-service
Suggested MCP Name: iblai-example-service
Base URL: https://api.example.com

========================================
Authentication Patterns Discovered
========================================
  - Type: bearer
    Header: Authorization
    Location: header

========================================
API Endpoints (3 found)
========================================

  GET /api/users/
  Tool name: get_api_users
  Query params: ['page', 'limit']

  POST /api/users/
  Tool name: create_api_users
  Has request body: Yes

  GET /api/users/{id}
  Tool name: get_api_users_id
  Path params: ['id']
```

### Step 3: Generate the MCP Server

```bash
python mcp-creator/cli.py create your-api.har --name myservice --output .
```

This creates a complete MCP server at `./iblai-myservice/` with:

```
iblai-myservice/
├── pyproject.toml
├── README.md
├── .env.example
└── iblai_myservice/
    ├── __init__.py
    ├── server.py      # MCP server with tool definitions
    ├── auth.py        # Authentication manager
    └── client.py      # HTTP client
```

### Step 4: Configure and Run

```bash
cd iblai-myservice
cp .env.example .env
# Edit .env with your authentication credentials
uv sync
uv run iblai-myservice
```

## Authentication

Generated MCP servers support multiple authentication methods via environment variables:

| Auth Type | Environment Variables |
|-----------|----------------------|
| API Key | `SERVICE_AUTH_TYPE=api_key`<br>`SERVICE_API_KEY=your_key` |
| Bearer Token | `SERVICE_AUTH_TYPE=bearer`<br>`SERVICE_BEARER_TOKEN=your_token` |
| Basic Auth | `SERVICE_AUTH_TYPE=basic`<br>`SERVICE_BASIC_USERNAME=user`<br>`SERVICE_BASIC_PASSWORD=pass` |
| Custom Header | `SERVICE_AUTH_TYPE=custom_header`<br>`SERVICE_CUSTOM_HEADER_NAME=X-Custom`<br>`SERVICE_CUSTOM_HEADER_VALUE=value` |
| OAuth2 Client Credentials | `SERVICE_AUTH_TYPE=oauth2_client_credentials`<br>`SERVICE_OAUTH2_CLIENT_ID=id`<br>`SERVICE_OAUTH2_CLIENT_SECRET=secret`<br>`SERVICE_OAUTH2_TOKEN_URL=https://...` |

Replace `SERVICE` with the uppercase service name (e.g., `BLOG` for iblai-blog).

## MCP Creator Reference

```bash
# Analyze a HAR file
python mcp-creator/cli.py analyze <har_file>
python mcp-creator/cli.py analyze <har_file> --json  # Output as JSON

# Generate an MCP server
python mcp-creator/cli.py create <har_file>
python mcp-creator/cli.py create <har_file> --name <service_name>
python mcp-creator/cli.py create <har_file> --output <directory>

# Quick usage
python mcp-creator/cli.py <har_file>              # Same as 'create'
python mcp-creator/cli.py <har_file> --analyze    # Same as 'analyze'
```

## Extending Generated Servers

Generated servers are starting points. Common extensions:

1. **Add custom tools**: Edit `server.py` to add tools not captured in the HAR
2. **Add MCP resources**: Expose data as MCP resources for context
3. **Add MCP prompts**: Create prompt templates for common operations
4. **Customize error handling**: Modify `client.py` for specific error responses
5. **Add rate limiting**: Implement rate limiting in the API client

## License

MIT
