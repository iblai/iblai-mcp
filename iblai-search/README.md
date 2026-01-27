# iblai-search

MCP (Model Context Protocol) server for IBL.ai search endpoints including mentor discovery, catalog search, and content recommendations.

**Base URL:** `https://asgi.data.iblai.app` (or your IBL.ai deployment)

**Type:** Hosted (no local installation required)

## Overview

The iblai-search server provides AI assistants with tools to search for mentors, courses, and get content recommendations. This enables intelligent discovery of learning resources within the IBL.ai platform.

## Configuration

### Authentication

The server uses Api-Token authentication via the `Authorization` header. You need a Platform API Key from your IBL.ai admin panel.

## Usage

### Connect from Claude Desktop / Cursor

Add this to your configuration file:

- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Desktop (Windows)**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Cursor**: Settings > Features > MCP Servers

```json
{
  "mcpServers": {
    "iblai-search": {
      "transport": "streamable-http",
      "url": "https://asgi.data.iblai.app/mcp/search/",
      "headers": {
        "Authorization": "Api-Token YOUR_API_TOKEN"
      }
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add iblai-search --transport http https://asgi.data.iblai.app/mcp/search/ --header "Authorization: Api-Token YOUR_API_TOKEN"
```

## Available Tools

### `get_catalog_search`

Search the course catalog for courses, programs, pathways, and skills.

**Endpoint:** GET /api/search/catalog/

**Parameters:**
- `query`: Search query string
- `limit`: Maximum number of results to return

**Returns:** Search results with courses, programs, pathways, and facets for filtering

---

### `get_mentor_search`

Search for mentors across the platform.

**Endpoint:** GET /api/ai-search/mentors/

**Parameters:**
- `query`: Search query string
- `limit`: Maximum number of results to return

**Returns:** List of mentors matching the query with metadata

---

### `get_recommendations`

Get AI-powered course recommendations.

**Endpoint:** GET /api/ai-search/recommendations/

**Parameters:**
- `limit`: Maximum number of recommendations
- `recommendation_type`: Type of recommendations (`mentors`, `courses`, `programs`, `resources`, `pathways`)

**Returns:** Personalized recommendations based on RAG search

---

### `ping`

Health check tool for the search MCP server.

**Parameters:** None

**Returns:** Current server timestamp in ISO format

---

## Use Cases

### Finding Relevant Mentors

Ask the AI assistant to find mentors on specific topics:

> "Find me mentors who specialize in machine learning and Python programming."

### Course Discovery

Search for courses matching your learning goals:

> "Search for beginner courses on data science."

### Content Recommendations

Get recommendations tailored to your platform:

> "What courses would you recommend for learning Python?"

## Error Handling

| Error Code | Description |
|------------|-------------|
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - User lacks permission for this resource |
| 404 | Not Found - Resource does not exist |
| 500 | Server Error - Contact support |

## Related MCP Servers

| Server | Description |
|--------|-------------|
| [iblai-analytics](../iblai-analytics) | Analytics and reporting tools |
| [iblai-agent-create](../iblai-agent-create) | Create and manage AI mentors |
| [iblai-agent-chat](../iblai-agent-chat) | Mentor chat interactions |

## License

Proprietary - IBL.ai
