#!/usr/bin/env python3
"""
iblai-instructure MCP Server

Auto-generated MCP server for Instructure Canvas LMS API.
Base URL: https://ibleducation.instructure.com
"""

import asyncio
import json
import os
from typing import Any

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .auth import AuthManager
from .client import APIClient

# Initialize the MCP server
server = Server("iblai-instructure")

# Initialize authentication manager
auth_manager = AuthManager()

# Initialize API client
client: APIClient | None = None


def get_client() -> APIClient:
    """Get or create the API client."""
    global client
    if client is None:
        client = APIClient(
            base_url=os.getenv("INSTRUCTURE_BASE_URL", "https://ibleducation.instructure.com"),
            auth_manager=auth_manager
        )
    return client


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available tools."""
    return [
        types.Tool(
            name="create_api_id_envelope",
            description="POST /api/{id}/envelope/",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}, "sentry_key": {"type": "string", "description": "Query parameter: sentry_key"}, "sentry_version": {"type": "string", "description": "Query parameter: sentry_version"}, "sentry_client": {"type": "string", "description": "Query parameter: sentry_client"}, "body": {"type": "object", "description": "Request body", "properties": {"raw": {"type": "string"}}}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_dashboard_dashboard_cards",
            description="GET /api/v1/dashboard/dashboard_cards",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_dashboard_sidebar",
            description="GET /dashboard-sidebar",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_dist_javascripts_translations_en_3f45f839b7_json",
            description="GET /dist/javascripts/translations/en-3f45f839b7.json",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_api_v1_release_notes_unread_count",
            description="GET /api/v1/release_notes/unread_count",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_api_v1_users_self_content_shares_unread_count",
            description="GET /api/v1/users/self/content_shares/unread_count",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_api_v1_conversations_unread_count",
            description="GET /api/v1/conversations/unread_count",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_api_v1_courses_id_activity_stream_summary",
            description="GET /api/v1/courses/{id}/activity_stream/summary",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_users_self_new_user_tutorial_statuses",
            description="GET /api/v1/users/self/new_user_tutorial_statuses",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_courses_id_modules_items_assignment_info",
            description="GET /courses/{id}/modules/items/assignment_info",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_courses_id_gradebook_user_ids",
            description="GET /courses/{id}/gradebook/user_ids",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_mentor_xblock_orgs_id_context",
            description="GET /api/mentor-xblock/orgs/{id}/context/",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}, "context_id": {"type": "string", "description": "Query parameter: context_id"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_courses_id_gradebook_filters",
            description="GET /api/v1/courses/{id}/gradebook_filters",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_courses_id_modules",
            description="GET /api/v1/courses/{id}/modules",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}, "per_page": {"type": "string", "description": "Query parameter: per_page"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_courses_id_custom_gradebook_columns",
            description="GET /api/v1/courses/{id}/custom_gradebook_columns",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}, "include_hidden": {"type": "string", "description": "Query parameter: include_hidden"}, "per_page": {"type": "string", "description": "Query parameter: per_page"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_courses_id_assignment_groups",
            description="GET /api/v1/courses/{id}/assignment_groups",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}, "exclude_assignment_submission_types[]": {"type": "string", "description": "Query parameter: exclude_assignment_submission_types[]"}, "exclude_response_fields[]": {"type": "string", "description": "Query parameter: exclude_response_fields[]"}, "include[]": {"type": "string", "description": "Query parameter: include[]"}, "override_assignment_dates": {"type": "string", "description": "Query parameter: override_assignment_dates"}, "hide_zero_point_quizzes": {"type": "string", "description": "Query parameter: hide_zero_point_quizzes"}, "per_page": {"type": "string", "description": "Query parameter: per_page"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_courses_id_users",
            description="GET /api/v1/courses/{id}/users",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}, "enrollment_state[]": {"type": "string", "description": "Query parameter: enrollment_state[]"}, "enrollment_type[]": {"type": "string", "description": "Query parameter: enrollment_type[]"}, "include[]": {"type": "string", "description": "Query parameter: include[]"}, "per_page": {"type": "string", "description": "Query parameter: per_page"}, "user_ids[]": {"type": "string", "description": "Query parameter: user_ids[]"}}, "required": ["id"]}
        ),
        types.Tool(
            name="get_api_v1_courses_id_students_submissions",
            description="GET /api/v1/courses/{id}/students/submissions",
            inputSchema={"type": "object", "properties": {"id": {"type": "string", "description": "Numeric identifier"}, "include[]": {"type": "string", "description": "Query parameter: include[]"}, "exclude_response_fields[]": {"type": "string", "description": "Query parameter: exclude_response_fields[]"}, "grouped": {"type": "string", "description": "Query parameter: grouped"}, "response_fields[]": {"type": "string", "description": "Query parameter: response_fields[]"}, "student_ids[]": {"type": "string", "description": "Query parameter: student_ids[]"}, "per_page": {"type": "string", "description": "Query parameter: per_page"}}, "required": ["id"]}
        ),
        types.Tool(
            name="create_api_graphql",
            description="POST /api/graphql",
            inputSchema={"properties": {"body": {"type": "object", "description": "Request body", "properties": {"operationName": {"type": "string"}, "variables": {"type": "object", "properties": {"courseId": {"type": "string"}, "studentId": {"type": "string"}}}, "query": {"type": "string"}}}}}
        )
    ]


@server.tool()
async def create_api_id_envelope(arguments: dict) -> list[types.TextContent]:
    """
    POST /api/{id}/envelope/ | Query params: sentry_key, sentry_version, sentry_client | Path params: id

    Endpoint: POST /api/{id}/envelope/
    """
    # Extract path parameters
    path = "/api/{id}/envelope/"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    if "sentry_key" in arguments:
            query_params["sentry_key"] = arguments["sentry_key"]
    if "sentry_version" in arguments:
            query_params["sentry_version"] = arguments["sentry_version"]
    if "sentry_client" in arguments:
            query_params["sentry_client"] = arguments["sentry_client"]

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="POST",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_dashboard_dashboard_cards(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/dashboard/dashboard_cards

    Endpoint: GET /api/v1/dashboard/dashboard_cards
    """
    # Extract path parameters
    path = "/api/v1/dashboard/dashboard_cards"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_dashboard_sidebar(arguments: dict) -> list[types.TextContent]:
    """
    GET /dashboard-sidebar

    Endpoint: GET /dashboard-sidebar
    """
    # Extract path parameters
    path = "/dashboard-sidebar"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_dist_javascripts_translations_en_3f45f839b7_json(arguments: dict) -> list[types.TextContent]:
    """
    GET /dist/javascripts/translations/en-3f45f839b7.json

    Endpoint: GET /dist/javascripts/translations/en-3f45f839b7.json
    """
    # Extract path parameters
    path = "/dist/javascripts/translations/en-3f45f839b7.json"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_release_notes_unread_count(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/release_notes/unread_count

    Endpoint: GET /api/v1/release_notes/unread_count
    """
    # Extract path parameters
    path = "/api/v1/release_notes/unread_count"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_users_self_content_shares_unread_count(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/users/self/content_shares/unread_count

    Endpoint: GET /api/v1/users/self/content_shares/unread_count
    """
    # Extract path parameters
    path = "/api/v1/users/self/content_shares/unread_count"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_conversations_unread_count(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/conversations/unread_count

    Endpoint: GET /api/v1/conversations/unread_count
    """
    # Extract path parameters
    path = "/api/v1/conversations/unread_count"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_courses_id_activity_stream_summary(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/courses/{id}/activity_stream/summary | Path params: id

    Endpoint: GET /api/v1/courses/{id}/activity_stream/summary
    """
    # Extract path parameters
    path = "/api/v1/courses/{id}/activity_stream/summary"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_users_self_new_user_tutorial_statuses(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/users/self/new_user_tutorial_statuses

    Endpoint: GET /api/v1/users/self/new_user_tutorial_statuses
    """
    # Extract path parameters
    path = "/api/v1/users/self/new_user_tutorial_statuses"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_courses_id_modules_items_assignment_info(arguments: dict) -> list[types.TextContent]:
    """
    GET /courses/{id}/modules/items/assignment_info | Path params: id

    Endpoint: GET /courses/{id}/modules/items/assignment_info
    """
    # Extract path parameters
    path = "/courses/{id}/modules/items/assignment_info"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_courses_id_gradebook_user_ids(arguments: dict) -> list[types.TextContent]:
    """
    GET /courses/{id}/gradebook/user_ids | Path params: id

    Endpoint: GET /courses/{id}/gradebook/user_ids
    """
    # Extract path parameters
    path = "/courses/{id}/gradebook/user_ids"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_mentor_xblock_orgs_id_context(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/mentor-xblock/orgs/{id}/context/ | Query params: context_id | Path params: id

    Endpoint: GET /api/mentor-xblock/orgs/{id}/context/
    """
    # Extract path parameters
    path = "/api/mentor-xblock/orgs/{id}/context/"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    if "context_id" in arguments:
            query_params["context_id"] = arguments["context_id"]

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_courses_id_gradebook_filters(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/courses/{id}/gradebook_filters | Path params: id

    Endpoint: GET /api/v1/courses/{id}/gradebook_filters
    """
    # Extract path parameters
    path = "/api/v1/courses/{id}/gradebook_filters"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_courses_id_modules(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/courses/{id}/modules | Query params: per_page | Path params: id

    Endpoint: GET /api/v1/courses/{id}/modules
    """
    # Extract path parameters
    path = "/api/v1/courses/{id}/modules"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    if "per_page" in arguments:
            query_params["per_page"] = arguments["per_page"]

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_courses_id_custom_gradebook_columns(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/courses/{id}/custom_gradebook_columns | Query params: include_hidden, per_page | Path params: id

    Endpoint: GET /api/v1/courses/{id}/custom_gradebook_columns
    """
    # Extract path parameters
    path = "/api/v1/courses/{id}/custom_gradebook_columns"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    if "include_hidden" in arguments:
            query_params["include_hidden"] = arguments["include_hidden"]
    if "per_page" in arguments:
            query_params["per_page"] = arguments["per_page"]

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_courses_id_assignment_groups(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/courses/{id}/assignment_groups | Query params: exclude_assignment_submission_types[], exclude_response_fields[], include[], override_assignment_dates, hide_zero_point_quizzes, per_page | Path params: id

    Endpoint: GET /api/v1/courses/{id}/assignment_groups
    """
    # Extract path parameters
    path = "/api/v1/courses/{id}/assignment_groups"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    if "exclude_assignment_submission_types[]" in arguments:
            query_params["exclude_assignment_submission_types[]"] = arguments["exclude_assignment_submission_types[]"]
    if "exclude_response_fields[]" in arguments:
            query_params["exclude_response_fields[]"] = arguments["exclude_response_fields[]"]
    if "include[]" in arguments:
            query_params["include[]"] = arguments["include[]"]
    if "override_assignment_dates" in arguments:
            query_params["override_assignment_dates"] = arguments["override_assignment_dates"]
    if "hide_zero_point_quizzes" in arguments:
            query_params["hide_zero_point_quizzes"] = arguments["hide_zero_point_quizzes"]
    if "per_page" in arguments:
            query_params["per_page"] = arguments["per_page"]

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_courses_id_users(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/courses/{id}/users | Query params: enrollment_state[], enrollment_type[], include[], per_page, user_ids[] | Path params: id

    Endpoint: GET /api/v1/courses/{id}/users
    """
    # Extract path parameters
    path = "/api/v1/courses/{id}/users"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    if "enrollment_state[]" in arguments:
            query_params["enrollment_state[]"] = arguments["enrollment_state[]"]
    if "enrollment_type[]" in arguments:
            query_params["enrollment_type[]"] = arguments["enrollment_type[]"]
    if "include[]" in arguments:
            query_params["include[]"] = arguments["include[]"]
    if "per_page" in arguments:
            query_params["per_page"] = arguments["per_page"]
    if "user_ids[]" in arguments:
            query_params["user_ids[]"] = arguments["user_ids[]"]

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def get_api_v1_courses_id_students_submissions(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/v1/courses/{id}/students/submissions | Query params: include[], exclude_response_fields[], grouped, response_fields[], student_ids[], per_page | Path params: id

    Endpoint: GET /api/v1/courses/{id}/students/submissions
    """
    # Extract path parameters
    path = "/api/v1/courses/{id}/students/submissions"
    if "id" in arguments:
            path = path.replace("{id}", str(arguments["id"]))

    # Extract query parameters
    query_params = {}
    if "include[]" in arguments:
            query_params["include[]"] = arguments["include[]"]
    if "exclude_response_fields[]" in arguments:
            query_params["exclude_response_fields[]"] = arguments["exclude_response_fields[]"]
    if "grouped" in arguments:
            query_params["grouped"] = arguments["grouped"]
    if "response_fields[]" in arguments:
            query_params["response_fields[]"] = arguments["response_fields[]"]
    if "student_ids[]" in arguments:
            query_params["student_ids[]"] = arguments["student_ids[]"]
    if "per_page" in arguments:
            query_params["per_page"] = arguments["per_page"]

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="GET",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


@server.tool()
async def create_api_graphql(arguments: dict) -> list[types.TextContent]:
    """
    POST /api/graphql

    Endpoint: POST /api/graphql
    """
    # Extract path parameters
    path = "/api/graphql"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    pass  # No query parameters

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="POST",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]



async def main():
    """Main entry point for the MCP server."""
    global client
    client = get_client()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
