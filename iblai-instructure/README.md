# iblai-instructure

MCP (Model Context Protocol) server for the Instructure Canvas LMS API.

**Base URL:** `https://ibleducation.instructure.com`

## Installation

```bash
cd iblai-instructure
uv sync
```

## Configuration

Canvas LMS uses Bearer token authentication. Generate an access token from your Canvas account settings.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `INSTRUCTURE_BASE_URL` | API base URL (default: https://ibleducation.instructure.com) | No |
| `INSTRUCTURE_AUTH_TYPE` | Set to `bearer` | Yes |
| `INSTRUCTURE_BEARER_TOKEN` | Canvas API access token | Yes |

### Example Configuration

```bash
export INSTRUCTURE_AUTH_TYPE=bearer
export INSTRUCTURE_BEARER_TOKEN=your_canvas_access_token
```

## Usage

### Local Installation

#### Claude Desktop

Add this to your Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "iblai-instructure": {
      "command": "uv",
      "args": ["run", "iblai-instructure"],
      "cwd": "/path/to/iblai-instructure"
    }
  }
}
```

#### Claude Code

```bash
claude mcp add iblai-instructure -- uv run --directory /path/to/iblai-instructure iblai-instructure
```

### Remote Server

If the MCP server is hosted on a remote server, configure the clients to connect via SSE:

#### Claude Desktop (Remote)

```json
{
  "mcpServers": {
    "iblai-instructure": {
      "url": "https://your-server.com/iblai-instructure/sse"
    }
  }
}
```

#### Claude Code (Remote)

```bash
claude mcp add iblai-instructure --transport sse https://your-server.com/iblai-instructure/sse
```

## Available Tools

### `create_api_id_envelope`

POST /api/{id}/envelope/

**Parameters:**
  - `id`: Numeric identifier (required)
  - `sentry_key`: Query parameter: sentry_key
  - `sentry_version`: Query parameter: sentry_version
  - `sentry_client`: Query parameter: sentry_client

### `get_api_v1_dashboard_dashboard_cards`

GET /api/v1/dashboard/dashboard_cards

**Parameters:**
  No parameters

### `get_dashboard_sidebar`

GET /dashboard-sidebar

**Parameters:**
  No parameters

### `get_dist_javascripts_translations_en_3f45f839b7_json`

GET /dist/javascripts/translations/en-3f45f839b7.json

**Parameters:**
  No parameters

### `get_api_v1_release_notes_unread_count`

GET /api/v1/release_notes/unread_count

**Parameters:**
  No parameters

### `get_api_v1_users_self_content_shares_unread_count`

GET /api/v1/users/self/content_shares/unread_count

**Parameters:**
  No parameters

### `get_api_v1_conversations_unread_count`

GET /api/v1/conversations/unread_count

**Parameters:**
  No parameters

### `get_api_v1_courses_id_activity_stream_summary`

GET /api/v1/courses/{id}/activity_stream/summary

**Parameters:**
  - `id`: Numeric identifier (required)

### `get_api_v1_users_self_new_user_tutorial_statuses`

GET /api/v1/users/self/new_user_tutorial_statuses

**Parameters:**
  No parameters

### `get_courses_id_modules_items_assignment_info`

GET /courses/{id}/modules/items/assignment_info

**Parameters:**
  - `id`: Numeric identifier (required)

### `get_courses_id_gradebook_user_ids`

GET /courses/{id}/gradebook/user_ids

**Parameters:**
  - `id`: Numeric identifier (required)

### `get_api_mentor_xblock_orgs_id_context`

GET /api/mentor-xblock/orgs/{id}/context/

**Parameters:**
  - `id`: Numeric identifier (required)
  - `context_id`: Query parameter: context_id

### `get_api_v1_courses_id_gradebook_filters`

GET /api/v1/courses/{id}/gradebook_filters

**Parameters:**
  - `id`: Numeric identifier (required)

### `get_api_v1_courses_id_modules`

GET /api/v1/courses/{id}/modules

**Parameters:**
  - `id`: Numeric identifier (required)
  - `per_page`: Query parameter: per_page

### `get_api_v1_courses_id_custom_gradebook_columns`

GET /api/v1/courses/{id}/custom_gradebook_columns

**Parameters:**
  - `id`: Numeric identifier (required)
  - `include_hidden`: Query parameter: include_hidden
  - `per_page`: Query parameter: per_page

### `get_api_v1_courses_id_assignment_groups`

GET /api/v1/courses/{id}/assignment_groups

**Parameters:**
  - `id`: Numeric identifier (required)
  - `exclude_assignment_submission_types[]`: Query parameter: exclude_assignment_submission_types[]
  - `exclude_response_fields[]`: Query parameter: exclude_response_fields[]
  - `include[]`: Query parameter: include[]
  - `override_assignment_dates`: Query parameter: override_assignment_dates
  - `hide_zero_point_quizzes`: Query parameter: hide_zero_point_quizzes
  - `per_page`: Query parameter: per_page

### `get_api_v1_courses_id_users`

GET /api/v1/courses/{id}/users

**Parameters:**
  - `id`: Numeric identifier (required)
  - `enrollment_state[]`: Query parameter: enrollment_state[]
  - `enrollment_type[]`: Query parameter: enrollment_type[]
  - `include[]`: Query parameter: include[]
  - `per_page`: Query parameter: per_page
  - `user_ids[]`: Query parameter: user_ids[]

### `get_api_v1_courses_id_students_submissions`

GET /api/v1/courses/{id}/students/submissions

**Parameters:**
  - `id`: Numeric identifier (required)
  - `include[]`: Query parameter: include[]
  - `exclude_response_fields[]`: Query parameter: exclude_response_fields[]
  - `grouped`: Query parameter: grouped
  - `response_fields[]`: Query parameter: response_fields[]
  - `student_ids[]`: Query parameter: student_ids[]
  - `per_page`: Query parameter: per_page

### `create_api_graphql`

POST /api/graphql

**Parameters:**
  No parameters


## Development

```bash
# Run the server directly
uv run iblai-instructure

# Run tests
uv run pytest
```

## License

MIT
