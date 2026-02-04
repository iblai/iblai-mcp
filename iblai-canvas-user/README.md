# iblai-canvas-user

MCP (Model Context Protocol) server for Canvas LMS account management, providing read-only access to Canvas accounts, settings, sub-accounts, and account-level course listings.

**Base URL:** `https://asgi.data.iblai.app` (or your IBL.ai deployment)

**Type:** Hosted (no local installation required)

## Overview

The iblai-canvas-user server enables AI assistants to query Canvas LMS account information through IBL.ai's proxy layer. It provides 14 read-only tools for account management including listing accounts, viewing settings, checking permissions, and browsing account-level course catalogs.

**Key Features:**
- Default account ID fallback from platform configuration
- Automatic credential resolution via PlatformApiKey
- Array parameter support for Canvas API filters

## Configuration

### Authentication

The server uses Api-Token authentication via the `Authorization` header. You need a Platform API Key from your IBL.ai admin panel. The platform must have a CanvasConfig record with valid Canvas credentials.

### Prerequisites

1. Platform API Key from IBL.ai admin panel
2. CanvasConfig record configured for the platform with:
   - Canvas host URL
   - Canvas access token
   - Default account ID in metadata (optional)

## Usage

### Connect from Claude Desktop / Cursor

Add this to your configuration file:

- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Desktop (Windows)**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Cursor**: Settings > Features > MCP Servers

```json
{
  "mcpServers": {
    "iblai-canvas-user": {
      "transport": "streamable-http",
      "url": "https://asgi.data.iblai.app/mcp/canvas-user/",
      "headers": {
        "Authorization": "Api-Token YOUR_API_TOKEN"
      }
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add iblai-canvas-user --transport http https://asgi.data.iblai.app/mcp/canvas-user/ --header "Authorization: Api-Token YOUR_API_TOKEN"
```

## Available Tools

### Utility

#### `ping`

Health check for the Canvas User MCP server.

**Parameters:** None

**Returns:** Current server timestamp in ISO format

---

### Account Listing

#### `list_accounts`

List accounts the current user can view or manage.

**Canvas API:** GET /api/v1/accounts

**Parameters:**
- `include`: Comma-separated list of additional data (lti_guid, registration_settings, services, course_count, sub_account_count)
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `get_manageable_accounts`

List accounts where the current user can create or manage courses.

**Canvas API:** GET /api/v1/manageable_accounts

**Parameters:**
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `get_course_creation_accounts`

List accounts where the current user can create courses.

**Canvas API:** GET /api/v1/course_creation_accounts

**Parameters:**
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `list_course_admin_accounts`

List accounts accessible through admin course enrollments (Teacher, TA, Designer).

**Canvas API:** GET /api/v1/course_accounts

**Parameters:**
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

### Single Account

#### `get_account`

Get a single account by ID. If omitted, uses the default account from Canvas config.

**Canvas API:** GET /api/v1/accounts/:id

**Parameters:**
- `id`: The Canvas account ID (optional - defaults to configured account)

---

#### `get_account_settings`

Get settings for an account. Requires manage_account_settings permission.

**Canvas API:** GET /api/v1/accounts/:account_id/settings

**Parameters:**
- `account_id`: The Canvas account ID (optional - defaults to configured account)

---

#### `get_environment_settings`

Get global environment settings for the root account.

**Canvas API:** GET /api/v1/settings/environment

**Parameters:** None

---

#### `get_account_permissions`

Get permission information for the calling user on a given account.

**Canvas API:** GET /api/v1/accounts/:account_id/permissions

**Parameters:**
- `account_id`: The Canvas account ID (optional - defaults to configured account)
- `permissions`: Comma-separated list of permission names to check

---

### Sub-Accounts

#### `get_sub_accounts`

List sub-accounts of a given account.

**Canvas API:** GET /api/v1/accounts/:account_id/sub_accounts

**Parameters:**
- `account_id`: The Canvas account ID (optional - defaults to configured account)
- `recursive`: If 'true', return entire account tree
- `order`: Sort by 'id' or 'name'
- `include`: Comma-separated list (course_count, sub_account_count)
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

### Account Resources

#### `get_terms_of_service`

Get the terms of service for an account.

**Canvas API:** GET /api/v1/accounts/:account_id/terms_of_service

**Parameters:**
- `account_id`: The Canvas account ID (optional - defaults to configured account)

---

#### `get_help_links`

Get help links configured for an account.

**Canvas API:** GET /api/v1/accounts/:account_id/help_links

**Parameters:**
- `account_id`: The Canvas account ID (optional - defaults to configured account)

---

#### `get_manually_created_courses_account`

Get the sub-account for manually created courses in the domain root account.

**Canvas API:** GET /api/v1/manually_created_courses_account

**Parameters:** None

---

### Account Courses

#### `list_account_courses`

List courses in an account with extensive filtering options.

**Canvas API:** GET /api/v1/accounts/:account_id/courses

**Parameters:**
- `account_id`: The Canvas account ID (optional - defaults to configured account)
- `with_enrollments`: Filter courses with/without enrollments ('true'/'false')
- `published`: Filter by published state ('true'/'false')
- `completed`: Filter by completed state ('true'/'false')
- `blueprint`: Filter blueprint courses ('true'/'false')
- `blueprint_associated`: Filter blueprint-associated courses ('true'/'false')
- `public`: Filter public courses ('true'/'false')
- `enrollment_term_id`: Filter by enrollment term ID
- `search_term`: Partial name/code/SIS ID match (min 3 chars)
- `sort`: Sort field (course_status, course_name, sis_course_id, teacher, account_name)
- `order`: Sort order (asc, desc)
- `search_by`: Search scope (course, teacher)
- `starts_before`: Filter courses starting before this date (YYYY-MM-DD)
- `ends_after`: Filter courses ending after this date (YYYY-MM-DD)
- `homeroom`: Filter homeroom courses ('true'/'false')
- `include`: Comma-separated list of additional data to include
- `state`: Comma-separated course states (created, claimed, available, completed, deleted, all)
- `enrollment_type`: Comma-separated enrollment types (teacher, student, ta, observer, designer)
- `by_teachers`: Comma-separated teacher user IDs to filter by
- `by_subaccounts`: Comma-separated sub-account IDs to filter by
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

## Use Cases

### Browse Organization Structure

> "List all accounts I have access to with their course counts."

### Check Permissions

> "What permissions do I have on the main account?"

### Find Courses

> "Show me all published courses in the account that start before March 2025."

### Explore Sub-Accounts

> "Get the full sub-account tree for the root account."

## Default Account ID

Many tools accept an optional `account_id` parameter. When omitted, the server automatically uses the default account ID stored in the platform's CanvasConfig metadata (`metadata.id`). This simplifies common operations by eliminating the need to specify the account ID for every call.

## Error Handling

| Error Code | Description |
|------------|-------------|
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - User lacks Canvas permission for this resource |
| 404 | Not Found - Account or resource does not exist |
| 500 | Server Error - Contact support |

Errors from the Canvas API are returned as string messages describing the issue.

## Related MCP Servers

| Server | Description |
|--------|-------------|
| [iblai-canvas-course](../iblai-canvas-course) | Course-level operations and user management |
| [iblai-analytics](../iblai-analytics) | Platform-wide analytics and metrics |
| [iblai-user](../iblai-user) | Learner profile and personal analytics |

## License

Proprietary - IBL.ai
