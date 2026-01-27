# iblai-agent-create

MCP (Model Context Protocol) server for creating and managing AI mentors, including CRUD operations, forking, and configuration.

**Base URL:** `https://asgi.data.iblai.app` (or your IBL.ai deployment)

**Type:** Hosted (no local installation required)

## Overview

The iblai-agent-create server enables AI assistants to create, configure, and manage AI mentors. This server provides full mentor lifecycle management including creation from templates, settings configuration, and document training.

Key features include:
- Create mentors from templates
- Configure LLM settings (provider, model, temperature)
- Manage display settings and feature flags
- Train mentors with documents, URLs, or text content
- Update mentor prompts and permissions

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
    "iblai-agent-create": {
      "transport": "streamable-http",
      "url": "https://asgi.data.iblai.app/mcp/agent-create/",
      "headers": {
        "Authorization": "Api-Token YOUR_API_TOKEN"
      }
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add iblai-agent-create --transport http https://asgi.data.iblai.app/mcp/agent-create/ --header "Authorization: Api-Token YOUR_API_TOKEN"
```

## Available Tools

### `ping`

Health check tool for the agent-create MCP server.

**Parameters:** None

**Returns:** Current server timestamp in ISO format

---

### `get_mentor_settings`

Retrieve mentor settings and configuration.

**Endpoint:** GET /api/ai-mentor/orgs/{org}/users/{user_id}/mentors/{mentor}/settings/

**Parameters:**
- `user_id`: User identifier (required)
- `mentor`: Mentor unique ID (required)

**Returns:** Complete mentor configuration including:
- Display settings (theme, colors, images)
- LLM configuration (provider, model, temperature)
- Feature flags (image generation, web browsing, code interpreter)
- Prompts (system, proactive, study mode)
- Visibility and permissions

---

### `post_mentor_with_settings`

Create a new mentor from a template.

**Endpoint:** POST /api/ai-mentor/orgs/{org}/users/{user_id}/mentor-with-settings/

**Parameters:**
- `user_id`: User identifier (required)
- `template_name`: Template to create mentor from (required)
- `new_mentor_name`: Name for the new mentor (required)
- `display_name`: Display name (optional)
- `description`: Mentor description (optional)
- `system_prompt`: Custom system prompt (optional)
- `llm_provider`: LLM provider to use (optional)

**Returns:** Created mentor object with unique_id, settings, and configuration

---

### `put_mentor_settings`

Update existing mentor settings.

**Endpoint:** PUT /api/ai-mentor/orgs/{org}/users/{user_id}/mentors/{mentor}/settings/

**Parameters:**
- `user_id`: User identifier (required)
- `mentor`: Mentor unique ID (required)
- `mentor_name`: New mentor name (optional)
- `display_name`: New display name (optional)
- `mentor_description`: New description (optional)
- `system_prompt`: New system prompt (optional)
- `llm_provider`: LLM provider (optional)
- `enable_image_generation`: Enable/disable image generation (optional)
- `enable_web_browsing`: Enable/disable web browsing (optional)
- `categories`: Mentor categories (optional)
- `types`: Mentor types (optional)
- `subjects`: Mentor subjects (optional)

**Returns:** Updated mentor settings object

---

### `post_train_document`

Train a document through worker process (for larger documents).

**Endpoint:** POST /api/ai-index/orgs/{org}/users/{user_id}/documents/train/

**Parameters:**
- `user_id`: User identifier (required)
- `type`: Document type - `file`, `url`, or `text` (required)
- `pathway`: Mentor unique ID to train (required)
- `url`: URL to train from (for url type)

**Returns:** Task confirmation or error message

**Note:** Use the mentor_id as the `pathway` parameter. The pathway must be a valid mentor unique ID (UUID format).

---

### `post_retriever_train`

Train a document directly (for smaller documents).

**Endpoint:** POST /api/ai-index/orgs/{org}/users/{user_id}/documents/train/retriever/

**Parameters:**
- `user_id`: User identifier (required)
- `pathway`: Mentor unique ID to train (required)
- `url`: URL to train from

**Returns:** `{"detail": "Document trained successfully"}`

---

## Use Cases

### Create a New Mentor

> "Create a new mentor for data science based on the ai-mentor template"

### Update Mentor Configuration

> "Update mentor settings for mentor ID 123 to enable web browsing"

### Train Mentor with Documents

> "Train the mentor with this documentation URL: https://example.com/docs"

### List Available Templates

> "Show me available mentor templates"

## Error Handling

| Error Code | Description |
|------------|-------------|
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - User lacks permission for this resource |
| 404 | Not Found - Mentor or resource does not exist |
| 422 | Validation Error - Invalid parameters |
| 500 | Server Error - Contact support |

### Common Errors

**"Document pathway is not a valid mentor unique id"**
- When using `post_train_document` or `post_retriever_train`, the `pathway` parameter must be a valid mentor UUID
- Use the mentor's unique ID (not the mentor name or slug)

**"We couldn't reach the website"**
- When training documents from URLs, ensure the URL is publicly accessible
- The URL may be blocked, require authentication, or be offline

## Related MCP Servers

| Server | Description |
|--------|-------------|
| [iblai-analytics](../iblai-analytics) | Monitor mentor usage and costs |
| [iblai-search](../iblai-search) | Discover available mentors |
| [iblai-agent-chat](../iblai-agent-chat) | Chat with mentors |

## License

Proprietary - IBL.ai
