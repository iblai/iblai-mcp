# iblai-blog

MCP (Model Context Protocol) server for the blog API.

**Base URL:** `https://blog.ibl.ai`

## Installation

```bash
cd iblai-blog
uv sync
```

## Configuration

No authentication was detected in the captured API calls. This API appears to be public.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BLOG_BASE_URL` | API base URL (default: https://blog.ibl.ai) | No |

## Usage

### Local Installation

#### Claude Desktop

Add this to your Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "iblai-blog": {
      "command": "uv",
      "args": ["run", "iblai-blog"],
      "cwd": "/path/to/iblai-blog"
    }
  }
}
```

#### Claude Code

```bash
claude mcp add iblai-blog -- uv run --directory /path/to/iblai-blog iblai-blog
```

### Remote Server

If the MCP server is hosted on a remote server, configure the clients to connect via SSE:

#### Claude Desktop (Remote)

```json
{
  "mcpServers": {
    "iblai-blog": {
      "url": "https://your-server.com/iblai-blog/sse"
    }
  }
}
```

#### Claude Code (Remote)

```bash
claude mcp add iblai-blog --transport sse https://your-server.com/iblai-blog/sse
```

## Available Tools

### `get_api_posts`

GET /api/posts/

**Parameters:**
  - `category__slug`: Query parameter: category__slug
  - `page`: Query parameter: page
  - `search`: Query parameter: search


## Development

```bash
# Run the server directly
uv run iblai-blog

# Run tests
uv run pytest
```

## License

MIT
