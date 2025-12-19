#!/usr/bin/env python3
"""
iblai-blog MCP Server

Auto-generated MCP server for blog API.
Base URL: https://blog.ibl.ai

Generated on: 2025-12-19T13:57:00.237400
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
server = Server("iblai-blog")

# Initialize authentication manager
auth_manager = AuthManager()

# Initialize API client
client: APIClient | None = None


def get_client() -> APIClient:
    """Get or create the API client."""
    global client
    if client is None:
        client = APIClient(
            base_url=os.getenv("BLOG_BASE_URL", "https://blog.ibl.ai"),
            auth_manager=auth_manager
        )
    return client


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available tools."""
    return [
        types.Tool(
            name="get_api_posts",
            description="GET /api/posts/",
            inputSchema={"type": "object", "properties": {"category__slug": {"type": "string", "description": "Query parameter: category__slug"}, "page": {"type": "string", "description": "Query parameter: page"}, "search": {"type": "string", "description": "Query parameter: search"}}}
        )
    ]


@server.tool()
async def get_api_posts(arguments: dict) -> list[types.TextContent]:
    """
    GET /api/posts/ | Query params: category__slug, page, search

    Endpoint: GET /api/posts/
    """
    # Extract path parameters
    path = "/api/posts/"
    pass  # No path parameters

    # Extract query parameters
    query_params = {}
    if "category__slug" in arguments:
            query_params["category__slug"] = arguments["category__slug"]
    if "page" in arguments:
            query_params["page"] = arguments["page"]
    if "search" in arguments:
            query_params["search"] = arguments["search"]

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
