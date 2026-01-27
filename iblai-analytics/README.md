# iblai-analytics

MCP (Model Context Protocol) server for IBL.ai analytics endpoints providing comprehensive insights into mentor interactions, user engagement, LLM costs, and learning patterns.

**Base URL:** `https://asgi.data.iblai.app` (or your IBL.ai deployment)

**Type:** Hosted (no local installation required)

## Overview

The iblai-analytics server enables AI assistants to access detailed analytics about mentor-student interactions, conversation patterns, topic analysis, sentiment tracking, and cost reporting. This is essential for administrators and educators monitoring platform usage and effectiveness.

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

## Available Tools

### User & Platform Information

#### `get_whoami`

Get the current authenticated username/user_id.

**Parameters:** None

**Returns:** Current user's username

---

#### `get_aboutme`

Get detailed information about the current user including platform memberships and admin privileges.

**Parameters:** None

**Returns:** User profile with platform affiliations

---

#### `count_users_in_platform`

Get the total count of active users in a platform.

**Parameters:**
- `platform`: Platform key/identifier (required)

**Returns:** Number of active users

---

#### `get_date`

Get the current server date and time.

**Parameters:** None

**Returns:** Current timestamp in ISO format

---

### Chat History & Conversations

#### `get_analytics_chathistory_list`

Retrieve chat message history for a user.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/chat-history/

**Parameters:**
- `user_id`: User identifier (required)
- `page`: Page number for pagination
- `page_size`: Results per page

---

#### `get_analytics_chathistory_filter`

Filter chat history with advanced criteria.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/chat-history-filter/

**Parameters:**
- `user_id`: User identifier (required)
- `mentor`: Filter by mentor ID
- `start_date`: Start date filter
- `end_date`: End date filter

---

#### `get_analytics_conversations`

Get conversation sessions for a user.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/conversation/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_conversations_messages`

Get detailed message transcripts from conversations.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/transcripts/

**Parameters:**
- `user_id`: User identifier (required)
- `session_id`: Specific session to retrieve

---

#### `get_analytics_conversation_summary`

Get summarized conversation data.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/conversation-summary/

**Parameters:**
- `user_id`: User identifier (required)

---

### Topic Analysis

#### `get_analytics_topics_summary`

Get a summary of topics discussed across conversations.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/topics/summary/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_most_discussed_topics`

Get the most frequently discussed topics.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/most-discussed-topics/

**Parameters:**
- `user_id`: User identifier (required)
- `limit`: Maximum number of topics to return

---

#### `get_analytics_topic_statistics`

Get paginated topic statistics.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/topic-statistics/

**Parameters:**
- `user_id`: User identifier (required)
- `page`: Page number
- `page_size`: Results per page

---

#### `get_analytics_topic_overview`

Get overview of topic distribution.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/topic-overview/

**Parameters:**
- `user_id`: User identifier (required)

---

### User Metrics & Engagement

#### `get_analytics_overview_summary`

Get overall analytics summary for the platform.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/overview-summary/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_usage_summary`

Get mentor usage summary for users.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/usage-summary/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_user_metrics`

Get detailed user engagement metrics.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/user-metrics/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_user_metrics_pie_chart`

Get user metrics formatted for pie chart visualization.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/user-metrics-pie-chart/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_average_messages_per_session`

Get average number of messages per chat session.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/average-messages-per-session/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_top_students_by_chat_messages`

Get ranking of students by chat activity.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/top-students-by-chat-messages/

**Parameters:**
- `user_id`: User identifier (required)
- `limit`: Maximum number of students to return

---

### User Trends & Cohorts

#### `get_analytics_registered_users_trend`

Get trend of user registrations over time.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/registered-users-trend/

**Parameters:**
- `user_id`: User identifier (required)
- `start_date`: Start date for trend
- `end_date`: End date for trend

---

#### `get_analytics_user_cohorts_over_time`

Get user cohort analysis over time.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/user-cohorts-over-time/

**Parameters:**
- `user_id`: User identifier (required)

---

### Mentor Analytics

#### `get_analytics_mentor_summary`

Get summary statistics for mentors.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/mentor-summary/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_mentor_detail`

Get detailed analytics for a specific mentor.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/mentor-detail/

**Parameters:**
- `user_id`: User identifier (required)
- `mentor_id`: Mentor unique identifier

---

#### `get_analytics_total_users_by_mentor`

Get user count breakdown by mentor.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/total-users-by-mentor/

**Parameters:**
- `user_id`: User identifier (required)

---

### Sentiment & Feedback

#### `get_analytics_user_sentiment`

Get sentiment analysis of user conversations.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/user-sentiment/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_sentiment_count`

Get count of sentiment categories.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/sentiment-count/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_rating_summary`

Get user rating summary for mentor interactions.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/rating-summary/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_user_rating`

Get user feedback ratings.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/user-feedback/

**Parameters:**
- `user_id`: User identifier (required)

---

### LLM Cost Tracking

#### `get_analytics_llm_cost_per_user`

Get LLM usage costs broken down by user.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/costs/peruser/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_llm_cost_per_mentor`

Get LLM usage costs broken down by mentor.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/costs/permentor/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_llm_model_cost`

Get LLM costs by model type.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/costs/model/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_llm_costs_per_tenant`

Get LLM costs across all tenants (admin only).

**Endpoint:** GET /api/ai-analytics/costs/pertenant/

**Parameters:** None (requires admin privileges)

---

#### `get_analytics_tenant_cost`

Get total LLM cost for a tenant.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/tenant-cost/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_user_cost`

Get LLM cost for a specific user.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/user-cost/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_mentor_cost`

Get LLM cost for a specific mentor.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/mentors/{mentor_unique_id}/cost/

**Parameters:**
- `user_id`: User identifier (required)
- `mentor_unique_id`: Mentor unique identifier (required)

---

### Traces & Observations (Debugging)

#### `get_analytics_traces_list`

Get execution traces for debugging.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/traces/

**Parameters:**
- `user_id`: User identifier (required)

---

#### `get_analytics_observations_list`

Get observations from execution traces.

**Endpoint:** GET /api/ai-analytics/orgs/{org}/users/{user_id}/observations/

**Parameters:**
- `user_id`: User identifier (required)

---

## Use Cases

### Monitor Platform Usage

> "Show me the overall analytics summary for our organization this month."

### Track LLM Costs

> "What are our LLM costs broken down by mentor?"

### Analyze User Engagement

> "Who are the most active students based on chat messages?"

### Understand Topics

> "What are the most discussed topics across all mentors?"

### Sentiment Analysis

> "What's the sentiment breakdown of user conversations this week?"

## Error Handling

| Error Code | Description |
|------------|-------------|
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - User lacks admin permission |
| 404 | Not Found - Resource does not exist |
| 500 | Server Error - Contact support |

## Related MCP Servers

| Server | Description |
|--------|-------------|
| [iblai-search](../iblai-search) | Search and discovery tools |
| [iblai-agent-create](../iblai-agent-create) | Create and manage AI mentors |
| [iblai-agent-chat](../iblai-agent-chat) | Mentor chat interactions |

## License

Proprietary - IBL.ai

