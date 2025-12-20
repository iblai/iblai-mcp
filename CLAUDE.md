# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains MCP (Model Context Protocol) servers for various APIs, all following the naming convention `iblai-<service>`.

## Commands

```bash
# Install dependencies
cd iblai-<service>
uv sync

# Run the server
uv run iblai-<service>

# Run tests
uv run pytest
```

## Server Structure

Each MCP server contains:

- **server.py**: MCP server with tool definitions, uses `@server.tool()` decorators
- **auth.py**: `AuthManager` class supporting multiple auth types (api_key, bearer, basic, custom_header, oauth2_client_credentials) via environment variables
- **client.py**: `APIClient` class for async HTTP requests with httpx

## Key Patterns

- Server names follow `iblai-<service>` convention
- Package names use underscores: `iblai_<service>`
- Auth is configured via environment variables: `<SERVICE>_AUTH_TYPE`, `<SERVICE>_API_KEY`, etc.
- MCP servers use stdio transport locally, SSE for remote hosting

## Creating New MCP Servers

Use the [iblai-mcp-creator](https://github.com/iblai/iblai-mcp-creator) tool to generate new MCP servers from HAR files.
