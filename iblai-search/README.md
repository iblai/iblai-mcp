# iblai-search

MCP (Model Context Protocol) server for IBL.ai search endpoints including mentor discovery, catalog search, and content recommendations.

**Base URL:** `https://base.manager.iblai.app` (or your IBL.ai deployment)

**Type:** Hosted (no local installation required)

## Overview

The iblai-search server provides AI assistants with tools to search for mentors, courses, and get personalized content recommendations. This enables intelligent discovery of learning resources within the IBL.ai platform.

## Configuration

### Authentication

The server uses Bearer token authentication. Users must authenticate via IBL.ai platform credentials.

## Usage

### Connect from Claude Desktop

Add this to your Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "iblai-search": {
      "url": "https://base.manager.iblai.app/mcp/search/sse"
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add iblai-search --transport sse https://base.manager.iblai.app/mcp/search/sse
```

### Connect from Cursor

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "iblai-search": {
      "url": "https://base.manager.iblai.app/mcp/search/sse"
    }
  }
}
```

## Available Tools

### Mentor Search Tools

#### `get_v2_global_mentor_search`

Search for mentors globally across the platform.

**Endpoint:** GET /api/ai-search/mentors/

**Parameters:**
- `org`: Organization/tenant identifier (required)
- `query`: Search query string
- `page`: Page number for pagination
- `page_size`: Number of results per page

---

#### `get_v2_personalized_mentors`

Get personalized mentor recommendations based on user preferences and history.

**Endpoint:** GET /api/ai-search/mentors/personalized/

**Parameters:**
- `org`: Organization/tenant identifier (required)
- `user_id`: User identifier (required)
- `page`: Page number for pagination
- `page_size`: Number of results per page

---

### Catalog Search Tools

#### `get_trigram_catalog_search`

Search the course catalog using trigram matching for fuzzy search.

**Endpoint:** GET /api/search/catalog/

**Parameters:**
- `org`: Organization/tenant identifier (required)
- `query`: Search query string
- `page`: Page number for pagination
- `page_size`: Number of results per page

---

#### `get_personalized_catalog_search`

Get personalized course recommendations from the catalog.

**Endpoint:** GET /api/search/personalized-catalog/

**Parameters:**
- `org`: Organization/tenant identifier (required)
- `user_id`: User identifier (required)
- `page`: Page number for pagination
- `page_size`: Number of results per page

---

### Recommendation Tools

#### `get_v2_recommendations`

Get AI-powered course recommendations for a user.

**Endpoint:** GET /api/ai-search/recommendations/

**Parameters:**
- `org`: Organization/tenant identifier (required)
- `user_id`: User identifier (required)
- `limit`: Maximum number of recommendations

---

### Health Check

#### `ping_search`

Simple health check tool for the search MCP server.

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

### Personalized Recommendations

Get recommendations tailored to your learning history:

> "What courses would you recommend for me based on my previous enrollments?"

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
| [iblai-mentorai-chat](../iblai-mentorai-chat) | Mentor chat interactions |

## License

Proprietary - IBL.ai

