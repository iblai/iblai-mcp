# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains MCP (Model Context Protocol) servers for various APIs, all following the naming convention `iblai-<service>`. It includes a code generator tool (`mcp-creator`) that automatically creates MCP servers from HAR files.

## Commands

### MCP Creator

```bash
# Analyze a HAR file to see discovered endpoints
python mcp-creator/cli.py analyze <har_file>

# Generate an MCP server from a HAR file
python mcp-creator/cli.py create <har_file> --name <service_name> --output .
```

### Generated MCP Servers

```bash
# Install dependencies
cd iblai-<service>
uv sync

# Run the server
uv run iblai-<service>

# Run tests
uv run pytest
```

## Architecture

### mcp-creator/

The code generator tool with three main components:

- **har_parser.py**: Parses HAR files to extract `ServiceInfo` containing endpoints, auth patterns, base URLs. Key classes: `HARParser`, `APIEndpoint`, `AuthPattern`, `ServiceInfo`
- **mcp_generator.py**: Generates complete MCP server packages from `ServiceInfo`. Creates server.py, auth.py, client.py, pyproject.toml, README.md
- **cli.py**: CLI interface with `analyze` and `create` commands

### Generated Server Structure (iblai-*/iblai_*/)

Each generated MCP server contains:

- **server.py**: MCP server with tool definitions, uses `@server.tool()` decorators
- **auth.py**: `AuthManager` class supporting multiple auth types (api_key, bearer, basic, custom_header, oauth2_client_credentials) via environment variables
- **client.py**: `APIClient` class for async HTTP requests with httpx

## Key Patterns

- Server names follow `iblai-<service>` convention
- Package names use underscores: `iblai_<service>`
- Auth is configured via environment variables: `<SERVICE>_AUTH_TYPE`, `<SERVICE>_API_KEY`, etc.
- Generated READMEs only document auth methods actually discovered in the HAR file
- MCP servers use stdio transport locally, SSE for remote hosting
