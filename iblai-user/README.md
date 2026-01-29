# iblai-user

MCP (Model Context Protocol) server for IBL.ai learner analytics and career profile management, providing personal analytics and professional profile tools for individual learners.

**Base URL:** `https://asgi.data.iblai.app` (or your IBL.ai deployment)

**Type:** Hosted (no local installation required)

## Overview

The iblai-user server enables AI assistants to access a learner's career profile (education, experience, resume, companies, institutions) and personal analytics (enrollments, grades, time spent, engagement). This is designed for learner-facing use cases where the user manages their own profile and views their own learning data.

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
    "iblai-user": {
      "transport": "streamable-http",
      "url": "https://asgi.data.iblai.app/mcp/user/",
      "headers": {
        "Authorization": "Api-Token YOUR_API_TOKEN"
      }
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add iblai-user --transport http https://asgi.data.iblai.app/mcp/user/ --header "Authorization: Api-Token YOUR_API_TOKEN"
```

## Available Tools

### Utility

#### `ping`

Health check for the User MCP server.

**Parameters:** None

**Returns:** Current server timestamp in ISO format

---

### Career Profile

#### `get_user_resume`

Fetch resume and media files for a user.

**Endpoint:** GET /api/career/resume/orgs/{org}/users/{username}/

**Parameters:**
- `username`: User's username (required)

---

#### `post_user_resume`

Upload a resume file.

**Endpoint:** POST /api/career/resume/orgs/{org}/users/{username}/

**Parameters:**
- `username`: User's username (required)

> **Note:** This endpoint expects multipart/form-data for file uploads.

---

#### `put_user_resume`

Update an existing resume.

**Endpoint:** PUT /api/career/resume/orgs/{org}/users/{username}/

**Parameters:**
- `username`: User's username (required)

> **Note:** This endpoint expects multipart/form-data for file uploads.

---

#### `get_company`

Fetch companies associated with a user.

**Endpoint:** GET /api/career/orgs/{org}/companies/users/{username}/

**Parameters:**
- `username`: User's username (required)

---

#### `post_company`

Create a new company entry.

**Endpoint:** POST /api/career/orgs/{org}/companies/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `name`: Company name (required)
- `industry`: Industry sector
- `website`: Company website URL

---

#### `put_company`

Update an existing company entry.

**Endpoint:** PUT /api/career/orgs/{org}/companies/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `id`: Company record ID (required)
- `name`: Company name (required)

---

#### `get_institution`

Fetch institutions list.

**Endpoint:** GET /api/career/orgs/{org}/institutions/users/{username}/

**Parameters:**
- `username`: User's username (required)

---

#### `post_institution`

Create a new institution entry.

**Endpoint:** POST /api/career/orgs/{org}/institutions/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `name`: Institution name (required)
- `institution_type`: Type (e.g. "university", "academy", "institute")
- `location`: Location
- `website`: Institution website URL

---

#### `put_institution`

Update an existing institution entry.

**Endpoint:** PUT /api/career/orgs/{org}/institutions/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `id`: Institution record ID (required)
- `name`: Institution name (required)

---

#### `get_education`

Fetch education records for a user.

**Endpoint:** GET /api/career/orgs/{org}/education/users/{username}/

**Parameters:**
- `username`: User's username (required)

---

#### `post_education`

Create a new education entry.

**Endpoint:** POST /api/career/orgs/{org}/education/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `institution_id`: Institution ID (required)
- `start_date`: Start date in YYYY-MM-DD format (required)
- `degree`: Degree name
- `field_of_study`: Field of study
- `end_date`: End date in YYYY-MM-DD format
- `description`: Description of studies

---

#### `put_education`

Update an existing education entry.

**Endpoint:** PUT /api/career/orgs/{org}/education/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `id`: Education record ID (required)
- `institution_id`: Institution ID (required)
- `start_date`: Start date in YYYY-MM-DD format (required)

---

#### `get_experience`

Fetch experience records for a user.

**Endpoint:** GET /api/career/orgs/{org}/experience/users/{username}/

**Parameters:**
- `username`: User's username (required)

---

#### `post_experience`

Create a new experience entry.

**Endpoint:** POST /api/career/orgs/{org}/experience/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `company_id`: Company ID (required)
- `title`: Job title (required)
- `start_date`: Start date in YYYY-MM-DD format (required)
- `employment_type`: Employment type (e.g. "Full-time", "Part-time")
- `location`: Work location
- `end_date`: End date in YYYY-MM-DD format
- `is_current`: Whether this is the current position
- `description`: Role description

---

#### `put_experience`

Update an existing experience entry.

**Endpoint:** PUT /api/career/orgs/{org}/experience/users/{username}/

**Parameters:**
- `username`: User's username (required)
- `id`: Experience record ID (required)
- `company_id`: Company ID (required)
- `title`: Job title (required)
- `start_date`: Start date in YYYY-MM-DD format (required)

---

### Learner Analytics

These endpoints use RBAC-based permissions (`IsPlatformAdminOfUser | IsSelfAccess`) and work with PlatformApiKey tokens.

#### `get_learner_analytics`

Get unified learner analytics including enrollments, grades, time spent, engagement index, and last access across platforms.

**Endpoint:** GET /api/analytics/learners/

**Parameters:**
- `username`: Learner username
- `limit`: Page size
- `page`: Page number
- `start_date`: Start date filter (ISO 8601)
- `end_date`: End date filter (ISO 8601)
- `date_filter`: Preset filter (`today`, `7d`, `30d`, `90d`)

**Returns:** User info, summary metrics, per-platform results with pagination

---

#### `get_learner_details`

Get detailed learner analytics across catalog, mentor, and credential data, including per-course breakdowns.

**Endpoint:** GET /api/analytics/learner/details

**Parameters:**
- `username`: Learner username (required)
- `start_date`: Start date filter (ISO 8601)
- `end_date`: End date filter (ISO 8601)
- `date_filter`: Preset filter (`today`, `7d`, `30d`, `90d`)
- `metrics`: Specific metrics to include

**Returns:** User info with detailed course-level analytics data

---

## Use Cases

### Manage Career Profile

> "Show me my education and experience records."

### Update Profile

> "Add my new position as Senior Engineer at Acme Corp starting January 2025."

### View Learning Progress

> "What are my enrollment stats and time spent across all platforms?"

### Course Details

> "Show me my detailed analytics including grades and engagement."

## Error Handling

| Error Code | Description |
|------------|-------------|
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - User lacks permission for this resource |
| 404 | Not Found - Resource does not exist |
| 415 | Unsupported Media Type - Resume endpoints require multipart/form-data |
| 500 | Server Error - Contact support |

## Related MCP Servers

| Server | Description |
|--------|-------------|
| [iblai-analytics](../iblai-analytics) | Platform-wide analytics and metrics |
| [iblai-search](../iblai-search) | Search and discovery tools |
| [iblai-agent-create](../iblai-agent-create) | Create and manage AI mentors |
| [iblai-agent-chat](../iblai-agent-chat) | Mentor chat interactions |

## License

Proprietary - IBL.ai
