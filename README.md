# iblai-mcp

A collection of MCP (Model Context Protocol) servers for various APIs.

## Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/iblai/iblai-mcp.git
cd iblai-mcp

# Install and run an MCP server (e.g., iblai-blog)
cd iblai-blog
uv sync
uv run iblai-blog
```

### Connect from Claude Desktop

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

### Connect from Claude Code

```bash
claude mcp add iblai-blog -- uv run --directory /path/to/iblai-mcp/iblai-blog iblai-blog
```

### Connect to a Remote MCP Server

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

### Standalone Servers (Local Installation)

| Server | Description | Base URL |
|--------|-------------|----------|
| [iblai-blog](./iblai-blog) | Blog API for IBL.ai | https://blog.ibl.ai |
| [iblai-instructure](./iblai-instructure) | Instructure Canvas LMS API | https://ibleducation.instructure.com |

### Hosted Servers (IBL.ai Platform)

These MCP servers are hosted on the IBL.ai platform and require no local installation:

| Server | Description | Endpoint |
|--------|-------------|----------|
| [iblai-search](./iblai-search) | Mentor discovery, catalog search, recommendations | `/mcp/search/sse` |
| [iblai-analytics](./iblai-analytics) | Analytics, metrics, costs, conversation insights | `/mcp/analytics/sse` |
| [iblai-mentorai-chat](./iblai-mentorai-chat) | Direct AI mentor interactions | `/mcp/mentor-chat/sse` |

## Server Structure

Each MCP server follows a consistent structure:

```
iblai-<service>/
├── pyproject.toml          # Project configuration
├── README.md               # Server-specific documentation
├── .env.example            # Environment variables template
└── iblai_<service>/
    ├── __init__.py
    ├── server.py           # MCP server with tool definitions
    ├── auth.py             # Authentication manager
    └── client.py           # HTTP client
```

## Authentication

MCP servers support multiple authentication methods via environment variables:

| Auth Type | Environment Variables |
|-----------|----------------------|
| API Key | `SERVICE_AUTH_TYPE=api_key`<br>`SERVICE_API_KEY=your_key` |
| Bearer Token | `SERVICE_AUTH_TYPE=bearer`<br>`SERVICE_BEARER_TOKEN=your_token` |
| Basic Auth | `SERVICE_AUTH_TYPE=basic`<br>`SERVICE_BASIC_USERNAME=user`<br>`SERVICE_BASIC_PASSWORD=pass` |
| Custom Header | `SERVICE_AUTH_TYPE=custom_header`<br>`SERVICE_CUSTOM_HEADER_NAME=X-Custom`<br>`SERVICE_CUSTOM_HEADER_VALUE=value` |
| OAuth2 Client Credentials | `SERVICE_AUTH_TYPE=oauth2_client_credentials`<br>`SERVICE_OAUTH2_CLIENT_ID=id`<br>`SERVICE_OAUTH2_CLIENT_SECRET=secret`<br>`SERVICE_OAUTH2_TOKEN_URL=https://...` |

Replace `SERVICE` with the uppercase service name (e.g., `BLOG` for iblai-blog).

## Creating New MCP Servers

Use the [iblai-mcp-creator](https://github.com/iblai/iblai-mcp-creator) tool to generate new MCP servers from HAR files captured from browser network activity.

## License

MIT
