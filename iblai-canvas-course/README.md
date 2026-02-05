# iblai-canvas-course

MCP (Model Context Protocol) server for Canvas LMS course operations, providing read-only access to courses, enrollments, users, activity streams, and course settings.

**Base URL:** `https://asgi.data.iblai.app` (or your IBL.ai deployment)

**Type:** Hosted (no local installation required)

## Overview

The iblai-canvas-course server enables AI assistants to query Canvas LMS course information through IBL.ai's proxy layer. It provides 20 read-only tools for course management including listing courses, viewing enrollments, checking user progress, and accessing activity streams.

**Key Features:**
- Course and user listing with extensive filters
- Progress tracking for individual users and bulk operations
- Activity stream access for course-specific updates
- Course settings and permissions queries

## Configuration

### Authentication

The server uses Api-Token authentication via the `Authorization` header. You need a Platform API Key from your IBL.ai admin panel. The platform must have a CanvasConfig record with valid Canvas credentials.

### Prerequisites

> **Important:** Before using this MCP server, you must have registered your Canvas LMS authentication configuration with the IBL.ai platform. This means a **CanvasConfig** record must exist for your platform — without it, the server cannot proxy requests to your Canvas instance. Contact your IBL.ai administrator if this has not been set up.

1. Platform API Key from IBL.ai admin panel
2. CanvasConfig record configured for the platform with:
   - Canvas host URL
   - Canvas access token

   Your Canvas admin must provide these credentials, and they must be registered in the IBL.ai platform's admin panel under the Canvas configuration for your platform.

## Usage

### Connect from Claude Desktop / Cursor

Add this to your configuration file:

- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Desktop (Windows)**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Cursor**: Settings > Features > MCP Servers

```json
{
  "mcpServers": {
    "iblai-canvas-course": {
      "transport": "streamable-http",
      "url": "https://asgi.data.iblai.app/mcp/canvas-course/",
      "headers": {
        "Authorization": "Api-Token YOUR_API_TOKEN"
      }
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add iblai-canvas-course --transport http https://asgi.data.iblai.app/mcp/canvas-course/ --header "Authorization: Api-Token YOUR_API_TOKEN"
```

## Available Tools

### Utility

#### `ping`

Health check for the Canvas Course MCP server.

**Parameters:** None

**Returns:** Current server timestamp in ISO format

---

### Course Listing

#### `list_courses`

List the current user's active courses.

**Canvas API:** GET /api/v1/courses

**Parameters:**
- `enrollment_type`: Filter by enrollment type (teacher, student, ta, observer, designer)
- `enrollment_role_id`: Filter by course-level role ID
- `enrollment_state`: Filter by enrollment state (active, invited_or_pending, completed)
- `exclude_blueprint_courses`: Exclude blueprint courses ('true'/'false')
- `include`: Comma-separated additional data (needs_grading_count, syllabus_body, public_description, total_scores, current_grading_period_scores, grading_periods, term, account, course_progress, sections, storage_quota_used_mb, total_students, passback_status, favorites, teachers, observed_users, course_image, banner_image, concluded, post_manually)
- `state`: Comma-separated course states (unpublished, available, completed, deleted)
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `list_user_courses`

List courses for a specific user.

**Canvas API:** GET /api/v1/users/:user_id/courses

**Parameters:**
- `user_id`: The Canvas user ID (required)
- `include`: Comma-separated additional data to include
- `state`: Comma-separated course states to filter by
- `enrollment_state`: Filter by enrollment state
- `homeroom`: Only return homeroom courses ('true'/'false')
- `account_id`: Filter by associated account ID
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `get_course`

Get a single course by ID.

**Canvas API:** GET /api/v1/courses/:id

**Parameters:**
- `id`: The Canvas course ID (required)
- `include`: Comma-separated additional data to include
- `teacher_limit`: Maximum number of teacher enrollments to show

---

### Course Users

#### `list_course_users`

List users enrolled in a course.

**Canvas API:** GET /api/v1/courses/:course_id/users

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `search_term`: Partial name or full ID match
- `sort`: Sort field (username, last_login, email, sis_id)
- `enrollment_type`: Comma-separated enrollment types to filter by
- `enrollment_role_id`: Filter by role ID
- `include`: Comma-separated additional data (enrollments, locked, avatar_url, test_student, bio, custom_links, current_grading_period_scores, uuid)
- `user_id`: Return page containing this specific user
- `user_ids`: Comma-separated user IDs to filter by
- `enrollment_state`: Comma-separated enrollment states (active, invited, rejected, completed, inactive)
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `get_course_user`

Get information on a single user in a course.

**Canvas API:** GET /api/v1/courses/:course_id/users/:id

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `id`: The Canvas user ID (required)
- `include`: Comma-separated additional data (enrollments, locked, avatar_url, test_student, bio, custom_links, current_grading_period_scores, uuid)

---

#### `list_recent_students`

List recently logged in students in a course, ordered by most recent login.

**Canvas API:** GET /api/v1/courses/:course_id/recent_students

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `search_content_share_users`

Search for users eligible for content sharing in a course.

**Canvas API:** GET /api/v1/courses/:course_id/content_share_users

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `search_term`: Term to find users by name (required)

---

#### `get_test_student`

Get the test student for a course. Creates one if it doesn't exist.

**Canvas API:** GET /api/v1/courses/:course_id/student_view_student

**Parameters:**
- `course_id`: The Canvas course ID (required)

---

### Progress Tracking

#### `get_user_progress`

Get progress information for a user in a course.

**Canvas API:** GET /api/v1/courses/:course_id/users/:user_id/progress

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `user_id`: The Canvas user ID (required)

---

#### `get_bulk_user_progress`

Get progress information for all users enrolled in a course.

**Canvas API:** GET /api/v1/courses/:course_id/bulk_user_progress

**Parameters:**
- `course_id`: The Canvas course ID (required)

---

### Activity & TODO

#### `get_course_activity_stream`

Get the current user's course-specific activity stream.

**Canvas API:** GET /api/v1/courses/:course_id/activity_stream

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `page`: Page number for pagination
- `per_page`: Number of results per page

---

#### `get_course_activity_stream_summary`

Get a summary of the current user's course-specific activity stream.

**Canvas API:** GET /api/v1/courses/:course_id/activity_stream/summary

**Parameters:**
- `course_id`: The Canvas course ID (required)

---

#### `get_course_todo`

Get the current user's TODO items for a course.

**Canvas API:** GET /api/v1/courses/:course_id/todo

**Parameters:**
- `course_id`: The Canvas course ID (required)

---

### Course Settings & Permissions

#### `get_course_settings`

Get settings for a course.

**Canvas API:** GET /api/v1/courses/:course_id/settings

**Parameters:**
- `course_id`: The Canvas course ID (required)

---

#### `get_course_permissions`

Get permission information for the calling user in a course.

**Canvas API:** GET /api/v1/courses/:course_id/permissions

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `permissions`: Comma-separated list of permission names to check

---

### Assignments

#### `get_effective_due_dates`

Get effective due dates for assignments in a course.

**Canvas API:** GET /api/v1/courses/:course_id/effective_due_dates

**Parameters:**
- `course_id`: The Canvas course ID (required)
- `assignment_ids`: Comma-separated assignment IDs to query

---

## Use Cases

### Browse My Courses

> "List all my active courses with their progress information."

### Check Student Progress

> "Show me the progress for all students in course 12345."

### View Activity

> "What's in my activity stream for the Introduction to Python course?"

### Find Course Members

> "List all teachers and TAs enrolled in course 67890."

### Check Due Dates

> "What are the effective due dates for assignments in this course?"

## Error Handling

| Error Code | Description |
|------------|-------------|
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - User lacks Canvas permission for this resource |
| 404 | Not Found - Course or resource does not exist |
| 500 | Server Error - Contact support |

Errors from the Canvas API are returned as string messages describing the issue.

## Related MCP Servers

| Server | Description |
|--------|-------------|
| [iblai-canvas-user](../iblai-canvas-user) | Account management and settings |
| [iblai-analytics](../iblai-analytics) | Platform-wide analytics and metrics |
| [iblai-user](../iblai-user) | Learner profile and personal analytics |

## License

Proprietary - IBL.ai
