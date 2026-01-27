# iblai-mcp

A collection of MCP (Model Context Protocol) servers for the ibl.ai platform.

## Available MCP Servers

These MCP servers are hosted on the IBL.ai platform and require no local installation:

| Server | Description | Endpoint |
|--------|-------------|----------|
| [iblai-analytics](./iblai-analytics) | Analytics, metrics, costs, conversation insights | `/mcp/analytics/` |
| [iblai-search](./iblai-search) | Mentor discovery, catalog search, recommendations | `/mcp/search/` |
| [iblai-agent-create](./iblai-agent-create) | Create and manage AI mentors | `/mcp/agent-create/` |
| [iblai-agent-chat](./iblai-agent-chat) | Direct AI mentor interactions | `/mcp/agent-chat/` |

## Quick Start

### Connect from Claude Desktop / Cursor

Add to your configuration file:

- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Desktop (Windows)**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Cursor**: Settings > Features > MCP Servers

```json
{
  "mcpServers": {
    "iblai-analytics": {
      "transport": "streamable-http",
      "url": "https://asgi.data.iblai.app/mcp/analytics/",
      "headers": {
        "Authorization": "Api-Token YOUR_API_TOKEN"
      }
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add iblai-analytics --transport http https://asgi.data.iblai.app/mcp/analytics/ --header "Authorization: Api-Token YOUR_API_TOKEN"
```

## Authentication

All hosted MCP servers use Api-Token authentication. You need a Platform API Key from your IBL.ai admin panel.

The `org` parameter is automatically determined from your API token - you don't need to provide it.

## License

Proprietary - IBL.ai
