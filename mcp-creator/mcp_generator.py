"""
MCP Server Generator

Generates comprehensive MCP servers from parsed HAR data.
Supports multiple authentication methods and creates well-documented,
production-ready MCP server code.
"""

import json
import os
import re
from datetime import datetime
from typing import Any

from har_parser import ServiceInfo, APIEndpoint, AuthPattern, RequestParam


class MCPGenerator:
    """Generates MCP server code from parsed service information."""

    def __init__(self, service_info: ServiceInfo, output_dir: str):
        self.service_info = service_info
        self.output_dir = output_dir
        self.server_name = f"iblai-{service_info.name}"

    def generate(self) -> str:
        """Generate the complete MCP server package."""
        server_dir = os.path.join(self.output_dir, self.server_name)
        os.makedirs(server_dir, exist_ok=True)

        # Generate all files
        self._generate_server_py(server_dir)
        self._generate_init_py(server_dir)
        self._generate_auth_py(server_dir)
        self._generate_client_py(server_dir)
        self._generate_pyproject_toml(server_dir)
        self._generate_readme(server_dir)
        self._generate_env_example(server_dir)

        return server_dir

    def _python_safe_name(self, name: str) -> str:
        """Convert a name to a Python-safe identifier."""
        # Replace non-alphanumeric with underscore
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure doesn't start with number
        if safe and safe[0].isdigit():
            safe = '_' + safe
        return safe.lower()

    def _format_docstring(self, text: str, indent: int = 4) -> str:
        """Format text as a Python docstring."""
        indent_str = ' ' * indent
        lines = text.split('\n')
        return '\n'.join(indent_str + line for line in lines)

    def _generate_param_schema(self, params: list[RequestParam]) -> dict:
        """Generate JSON schema for parameters."""
        if not params:
            return {}

        properties = {}
        required = []

        for param in params:
            prop = {
                "type": "string",
                "description": param.description or f"Parameter: {param.name}"
            }

            # Add example if available
            if param.example_value is not None:
                if isinstance(param.example_value, str):
                    prop["type"] = "string"
                elif isinstance(param.example_value, int):
                    prop["type"] = "integer"
                elif isinstance(param.example_value, float):
                    prop["type"] = "number"
                elif isinstance(param.example_value, bool):
                    prop["type"] = "boolean"

            properties[param.name] = prop

            if param.required:
                required.append(param.name)

        schema = {
            "type": "object",
            "properties": properties
        }
        if required:
            schema["required"] = required

        return schema

    def _generate_body_schema(self, body: dict | None) -> dict:
        """Generate JSON schema from request body example."""
        if not body:
            return {}

        def infer_schema(value: Any) -> dict:
            if isinstance(value, dict):
                return {
                    "type": "object",
                    "properties": {
                        k: infer_schema(v) for k, v in value.items()
                    }
                }
            elif isinstance(value, list):
                if value:
                    return {
                        "type": "array",
                        "items": infer_schema(value[0])
                    }
                return {"type": "array", "items": {}}
            elif isinstance(value, bool):
                return {"type": "boolean"}
            elif isinstance(value, int):
                return {"type": "integer"}
            elif isinstance(value, float):
                return {"type": "number"}
            else:
                return {"type": "string"}

        return infer_schema(body)

    def _generate_tool_code(self, endpoint: APIEndpoint) -> str:
        """Generate the tool definition code for an endpoint."""
        tool_name = endpoint.tool_name
        safe_name = self._python_safe_name(tool_name)

        # Build description
        desc_parts = [f"{endpoint.method} {endpoint.path}"]
        if endpoint.query_params:
            desc_parts.append(f"Query params: {', '.join(p.name for p in endpoint.query_params)}")
        if endpoint.path_params:
            desc_parts.append(f"Path params: {', '.join(p.name for p in endpoint.path_params)}")

        description = " | ".join(desc_parts)

        # Build input schema
        all_params = endpoint.path_params + endpoint.query_params
        schema = self._generate_param_schema(all_params)

        if endpoint.request_body:
            body_schema = self._generate_body_schema(endpoint.request_body)
            if body_schema.get("properties"):
                schema.setdefault("properties", {})
                schema["properties"]["body"] = {
                    "type": "object",
                    "description": "Request body",
                    "properties": body_schema.get("properties", {})
                }

        schema_str = json.dumps(schema, indent=8) if schema else "{}"

        return f'''
@server.tool()
async def {safe_name}(arguments: dict) -> list[types.TextContent]:
    """
    {description}

    Endpoint: {endpoint.method} {endpoint.path}
    """
    # Extract path parameters
    path = "{endpoint.path}"
    {self._generate_path_param_extraction(endpoint.path_params)}

    # Extract query parameters
    query_params = {{}}
    {self._generate_query_param_extraction(endpoint.query_params)}

    # Extract body if present
    body = arguments.get("body")

    # Make the API request
    result = await client.request(
        method="{endpoint.method}",
        path=path,
        query_params=query_params,
        body=body
    )

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
'''

    def _generate_path_param_extraction(self, params: list[RequestParam]) -> str:
        """Generate code to extract and substitute path parameters."""
        if not params:
            return "pass  # No path parameters"

        lines = []
        for param in params:
            lines.append(f'if "{param.name}" in arguments:')
            lines.append(f'        path = path.replace("{{{param.name}}}", str(arguments["{param.name}"]))')

        return "\n    ".join(lines)

    def _generate_query_param_extraction(self, params: list[RequestParam]) -> str:
        """Generate code to extract query parameters."""
        if not params:
            return "pass  # No query parameters"

        lines = []
        for param in params:
            lines.append(f'if "{param.name}" in arguments:')
            lines.append(f'        query_params["{param.name}"] = arguments["{param.name}"]')

        return "\n    ".join(lines)

    def _generate_tools_list(self) -> str:
        """Generate the tools list for the server."""
        tools = []
        for endpoint in self.service_info.endpoints:
            tool_name = endpoint.tool_name

            # Build description
            desc_parts = [f"{endpoint.method} {endpoint.path}"]

            all_params = endpoint.path_params + endpoint.query_params
            schema = self._generate_param_schema(all_params)

            if endpoint.request_body:
                body_schema = self._generate_body_schema(endpoint.request_body)
                if body_schema.get("properties"):
                    schema.setdefault("properties", {})
                    schema["properties"]["body"] = {
                        "type": "object",
                        "description": "Request body",
                        "properties": body_schema.get("properties", {})
                    }

            tools.append({
                "name": tool_name,
                "description": " | ".join(desc_parts),
                "inputSchema": schema if schema else {"type": "object", "properties": {}}
            })

        return json.dumps(tools, indent=4)

    def _generate_server_py(self, server_dir: str) -> None:
        """Generate the main server.py file."""
        tools_code = "\n".join(
            self._generate_tool_code(ep) for ep in self.service_info.endpoints
        )

        content = f'''#!/usr/bin/env python3
"""
{self.server_name} MCP Server

Auto-generated MCP server for {self.service_info.name} API.
Base URL: {self.service_info.base_url}

Generated on: {datetime.now().isoformat()}
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
server = Server("{self.server_name}")

# Initialize authentication manager
auth_manager = AuthManager()

# Initialize API client
client: APIClient | None = None


def get_client() -> APIClient:
    """Get or create the API client."""
    global client
    if client is None:
        client = APIClient(
            base_url=os.getenv("{self._env_var_name("BASE_URL")}", "{self.service_info.base_url}"),
            auth_manager=auth_manager
        )
    return client


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available tools."""
    return [
        {self._generate_tools_list_items()}
    ]

{tools_code}


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
'''
        self._write_file(server_dir, "server.py", content)

    def _generate_tools_list_items(self) -> str:
        """Generate tool definitions for list_tools."""
        items = []
        for endpoint in self.service_info.endpoints:
            tool_name = endpoint.tool_name

            desc_parts = [f"{endpoint.method} {endpoint.path}"]
            description = " | ".join(desc_parts)

            all_params = endpoint.path_params + endpoint.query_params
            schema = self._generate_param_schema(all_params)

            if endpoint.request_body:
                body_schema = self._generate_body_schema(endpoint.request_body)
                if body_schema.get("properties"):
                    schema.setdefault("properties", {})
                    schema["properties"]["body"] = {
                        "type": "object",
                        "description": "Request body",
                        "properties": body_schema.get("properties", {})
                    }

            if not schema:
                schema = {"type": "object", "properties": {}}

            items.append(f'''types.Tool(
            name="{tool_name}",
            description="{description}",
            inputSchema={json.dumps(schema)}
        )''')

        return ",\n        ".join(items)

    def _env_var_name(self, suffix: str) -> str:
        """Generate environment variable name."""
        prefix = self.service_info.name.upper().replace('-', '_').replace('.', '_')
        return f"{prefix}_{suffix}"

    def _generate_init_py(self, server_dir: str) -> None:
        """Generate __init__.py file."""
        content = f'''"""
{self.server_name} MCP Server Package
"""

from .server import server, main

__all__ = ["server", "main"]
__version__ = "0.1.0"
'''
        self._write_file(server_dir, "__init__.py", content)

    def _generate_auth_py(self, server_dir: str) -> None:
        """Generate the authentication module."""
        env_prefix = self.service_info.name.upper().replace('-', '_').replace('.', '_')

        content = f'''"""
Authentication Manager for {self.server_name}

Supports multiple authentication methods:
- API Key authentication
- Bearer token authentication
- Basic authentication
- Custom header authentication
- OAuth2 (client credentials flow)
"""

import base64
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any


class AuthType(Enum):
    """Supported authentication types."""
    NONE = "none"
    API_KEY = "api_key"
    BEARER = "bearer"
    BASIC = "basic"
    CUSTOM_HEADER = "custom_header"
    OAUTH2_CLIENT_CREDENTIALS = "oauth2_client_credentials"


@dataclass
class AuthConfig:
    """Authentication configuration."""
    auth_type: AuthType = AuthType.NONE
    api_key: str | None = None
    api_key_header: str = "X-API-Key"
    bearer_token: str | None = None
    basic_username: str | None = None
    basic_password: str | None = None
    custom_header_name: str | None = None
    custom_header_value: str | None = None
    oauth2_client_id: str | None = None
    oauth2_client_secret: str | None = None
    oauth2_token_url: str | None = None
    oauth2_scope: str | None = None


class AuthManager:
    """
    Manages authentication for API requests.

    Supports multiple authentication methods and automatically
    applies the appropriate headers based on configuration.
    """

    def __init__(self, config: AuthConfig | None = None):
        """Initialize the auth manager with optional config."""
        self.config = config or self._load_from_env()
        self._oauth2_token: str | None = None
        self._token_expiry: float = 0

    def _load_from_env(self) -> AuthConfig:
        """Load authentication configuration from environment variables."""
        auth_type_str = os.getenv("{env_prefix}_AUTH_TYPE", "none").lower()

        try:
            auth_type = AuthType(auth_type_str)
        except ValueError:
            auth_type = AuthType.NONE

        return AuthConfig(
            auth_type=auth_type,
            api_key=os.getenv("{env_prefix}_API_KEY"),
            api_key_header=os.getenv("{env_prefix}_API_KEY_HEADER", "X-API-Key"),
            bearer_token=os.getenv("{env_prefix}_BEARER_TOKEN"),
            basic_username=os.getenv("{env_prefix}_BASIC_USERNAME"),
            basic_password=os.getenv("{env_prefix}_BASIC_PASSWORD"),
            custom_header_name=os.getenv("{env_prefix}_CUSTOM_HEADER_NAME"),
            custom_header_value=os.getenv("{env_prefix}_CUSTOM_HEADER_VALUE"),
            oauth2_client_id=os.getenv("{env_prefix}_OAUTH2_CLIENT_ID"),
            oauth2_client_secret=os.getenv("{env_prefix}_OAUTH2_CLIENT_SECRET"),
            oauth2_token_url=os.getenv("{env_prefix}_OAUTH2_TOKEN_URL"),
            oauth2_scope=os.getenv("{env_prefix}_OAUTH2_SCOPE"),
        )

    def get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers based on current configuration."""
        if self.config.auth_type == AuthType.NONE:
            return {{}}

        elif self.config.auth_type == AuthType.API_KEY:
            if self.config.api_key:
                return {{self.config.api_key_header: self.config.api_key}}
            return {{}}

        elif self.config.auth_type == AuthType.BEARER:
            if self.config.bearer_token:
                return {{"Authorization": f"Bearer {{self.config.bearer_token}}"}}
            return {{}}

        elif self.config.auth_type == AuthType.BASIC:
            if self.config.basic_username and self.config.basic_password:
                credentials = f"{{self.config.basic_username}}:{{self.config.basic_password}}"
                encoded = base64.b64encode(credentials.encode()).decode()
                return {{"Authorization": f"Basic {{encoded}}"}}
            return {{}}

        elif self.config.auth_type == AuthType.CUSTOM_HEADER:
            if self.config.custom_header_name and self.config.custom_header_value:
                return {{self.config.custom_header_name: self.config.custom_header_value}}
            return {{}}

        elif self.config.auth_type == AuthType.OAUTH2_CLIENT_CREDENTIALS:
            token = self._get_oauth2_token()
            if token:
                return {{"Authorization": f"Bearer {{token}}"}}
            return {{}}

        return {{}}

    def _get_oauth2_token(self) -> str | None:
        """Get OAuth2 token, refreshing if necessary."""
        import time

        # Return cached token if still valid
        if self._oauth2_token and time.time() < self._token_expiry - 60:
            return self._oauth2_token

        # Fetch new token
        if not all([
            self.config.oauth2_client_id,
            self.config.oauth2_client_secret,
            self.config.oauth2_token_url
        ]):
            return None

        try:
            import httpx

            data = {{
                "grant_type": "client_credentials",
                "client_id": self.config.oauth2_client_id,
                "client_secret": self.config.oauth2_client_secret,
            }}

            if self.config.oauth2_scope:
                data["scope"] = self.config.oauth2_scope

            with httpx.Client() as client:
                response = client.post(
                    self.config.oauth2_token_url,
                    data=data,
                    headers={{"Content-Type": "application/x-www-form-urlencoded"}}
                )
                response.raise_for_status()

                token_data = response.json()
                self._oauth2_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)
                self._token_expiry = time.time() + expires_in

                return self._oauth2_token

        except Exception as e:
            print(f"OAuth2 token fetch failed: {{e}}")
            return None

    def is_configured(self) -> bool:
        """Check if authentication is properly configured."""
        if self.config.auth_type == AuthType.NONE:
            return True

        elif self.config.auth_type == AuthType.API_KEY:
            return bool(self.config.api_key)

        elif self.config.auth_type == AuthType.BEARER:
            return bool(self.config.bearer_token)

        elif self.config.auth_type == AuthType.BASIC:
            return bool(self.config.basic_username and self.config.basic_password)

        elif self.config.auth_type == AuthType.CUSTOM_HEADER:
            return bool(self.config.custom_header_name and self.config.custom_header_value)

        elif self.config.auth_type == AuthType.OAUTH2_CLIENT_CREDENTIALS:
            return bool(
                self.config.oauth2_client_id and
                self.config.oauth2_client_secret and
                self.config.oauth2_token_url
            )

        return False
'''
        self._write_file(server_dir, "auth.py", content)

    def _generate_client_py(self, server_dir: str) -> None:
        """Generate the API client module."""
        content = f'''"""
API Client for {self.server_name}

Handles HTTP requests to the API with authentication,
error handling, and response parsing.
"""

import json
from typing import Any
from urllib.parse import urlencode

import httpx

from .auth import AuthManager


class APIError(Exception):
    """API request error."""

    def __init__(self, status_code: int, message: str, response_body: Any = None):
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"API Error {{status_code}}: {{message}}")


class APIClient:
    """
    HTTP client for making API requests.

    Handles authentication, request formatting, and error handling.
    """

    def __init__(
        self,
        base_url: str,
        auth_manager: AuthManager,
        timeout: float = 30.0
    ):
        """Initialize the API client."""
        self.base_url = base_url.rstrip('/')
        self.auth_manager = auth_manager
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=True
            )
        return self._client

    async def request(
        self,
        method: str,
        path: str,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> Any:
        """
        Make an API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: API endpoint path
            query_params: Optional query parameters
            body: Optional request body (will be JSON encoded)
            headers: Optional additional headers

        Returns:
            Parsed JSON response or raw text

        Raises:
            APIError: If the request fails
        """
        client = await self._get_client()

        # Build URL
        url = f"{{self.base_url}}{{path}}"
        if query_params:
            # Filter out None values
            filtered_params = {{k: v for k, v in query_params.items() if v is not None}}
            if filtered_params:
                url = f"{{url}}?{{urlencode(filtered_params)}}"

        # Build headers
        request_headers = {{
            "Accept": "application/json",
            "Content-Type": "application/json",
        }}

        # Add auth headers
        auth_headers = self.auth_manager.get_auth_headers()
        request_headers.update(auth_headers)

        # Add custom headers
        if headers:
            request_headers.update(headers)

        # Make request
        try:
            if body:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=body
                )
            else:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=request_headers
                )

            # Handle response
            if response.status_code >= 400:
                try:
                    error_body = response.json()
                except Exception:
                    error_body = response.text

                raise APIError(
                    status_code=response.status_code,
                    message=f"Request failed: {{response.status_code}}",
                    response_body=error_body
                )

            # Parse response
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return {{"text": response.text, "status_code": response.status_code}}

        except httpx.TimeoutException as e:
            raise APIError(
                status_code=408,
                message=f"Request timed out: {{str(e)}}"
            )
        except httpx.RequestError as e:
            raise APIError(
                status_code=0,
                message=f"Request failed: {{str(e)}}"
            )

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
'''
        self._write_file(server_dir, "client.py", content)

    def _generate_pyproject_toml(self, server_dir: str) -> None:
        """Generate pyproject.toml file."""
        content = f'''[project]
name = "{self.server_name}"
version = "0.1.0"
description = "MCP server for {self.service_info.name} API"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
]

[project.scripts]
{self.server_name} = "{self.server_name.replace('-', '_')}.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{self.server_name.replace('-', '_')}"]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
]
'''
        # Create proper package structure
        package_dir = os.path.join(server_dir, self.server_name.replace('-', '_'))
        os.makedirs(package_dir, exist_ok=True)

        # Move Python files to package directory
        for filename in ['server.py', '__init__.py', 'auth.py', 'client.py']:
            src = os.path.join(server_dir, filename)
            dst = os.path.join(package_dir, filename)
            if os.path.exists(src):
                os.rename(src, dst)

        self._write_file(server_dir, "pyproject.toml", content)

    def _generate_readme(self, server_dir: str) -> None:
        """Generate README.md file."""
        env_prefix = self.service_info.name.upper().replace('-', '_').replace('.', '_')

        # Generate tools documentation
        tools_docs = []
        for endpoint in self.service_info.endpoints:
            params = []
            for p in endpoint.path_params + endpoint.query_params:
                req = " (required)" if p.required else ""
                params.append(f"  - `{p.name}`: {p.description}{req}")

            params_str = "\n".join(params) if params else "  No parameters"

            tools_docs.append(f'''### `{endpoint.tool_name}`

{endpoint.method} {endpoint.path}

**Parameters:**
{params_str}
''')

        tools_section = "\n".join(tools_docs)

        # Generate authentication section based on discovered patterns
        auth_section = self._generate_auth_readme_section(env_prefix)

        # Generate Claude Desktop config based on discovered auth
        claude_config = self._generate_claude_desktop_config(env_prefix)

        content = f'''# {self.server_name}

MCP (Model Context Protocol) server for the {self.service_info.name} API.

**Base URL:** `{self.service_info.base_url}`

## Installation

```bash
cd {self.server_name}
uv sync
```

{auth_section}

## Usage

### Local Installation

#### Claude Desktop

Add this to your Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`

{claude_config}

#### Claude Code

```bash
claude mcp add {self.server_name} -- uv run --directory /path/to/{self.server_name} {self.server_name}
```

### Remote Server

If the MCP server is hosted on a remote server, configure the clients to connect via SSE:

#### Claude Desktop (Remote)

```json
{{
  "mcpServers": {{
    "{self.server_name}": {{
      "url": "https://your-server.com/{self.server_name}/sse"
    }}
  }}
}}
```

#### Claude Code (Remote)

```bash
claude mcp add {self.server_name} --transport sse https://your-server.com/{self.server_name}/sse
```

## Available Tools

{tools_section}

## Development

```bash
# Run the server directly
uv run {self.server_name}

# Run tests
uv run pytest
```

## License

MIT
'''
        self._write_file(server_dir, "README.md", content)

    def _generate_auth_readme_section(self, env_prefix: str) -> str:
        """Generate authentication section based on discovered patterns."""
        auth_patterns = self.service_info.auth_patterns

        if not auth_patterns:
            # No auth discovered - API appears to be public
            return f'''## Configuration

No authentication was detected in the captured API calls. This API appears to be public.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `{env_prefix}_BASE_URL` | API base URL (default: {self.service_info.base_url}) | No |'''

        # Auth was discovered - document what was found
        lines = ['''## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|''']

        lines.append(f'| `{env_prefix}_BASE_URL` | API base URL (default: {self.service_info.base_url}) | No |')

        # Document each discovered auth pattern
        for auth in auth_patterns:
            if auth.auth_type == 'bearer':
                lines.append(f'| `{env_prefix}_AUTH_TYPE` | Set to `bearer` | Yes |')
                lines.append(f'| `{env_prefix}_BEARER_TOKEN` | Bearer token for authentication | Yes |')
            elif auth.auth_type == 'api_key':
                lines.append(f'| `{env_prefix}_AUTH_TYPE` | Set to `api_key` | Yes |')
                lines.append(f'| `{env_prefix}_API_KEY` | API key for authentication | Yes |')
                if auth.header_name and auth.header_name != 'X-API-Key':
                    lines.append(f'| `{env_prefix}_API_KEY_HEADER` | Header name (default: {auth.header_name}) | No |')
            elif auth.auth_type == 'custom_header':
                lines.append(f'| `{env_prefix}_AUTH_TYPE` | Set to `custom_header` | Yes |')
                lines.append(f'| `{env_prefix}_CUSTOM_HEADER_NAME` | Header name: `{auth.header_name}` | Yes |')
                lines.append(f'| `{env_prefix}_CUSTOM_HEADER_VALUE` | Header value | Yes |')

        # Add example configuration
        example_lines = ['\n### Example Configuration\n\n```bash']
        for auth in auth_patterns:
            if auth.auth_type == 'bearer':
                example_lines.append(f'export {env_prefix}_AUTH_TYPE=bearer')
                example_lines.append(f'export {env_prefix}_BEARER_TOKEN=your_token_here')
            elif auth.auth_type == 'api_key':
                example_lines.append(f'export {env_prefix}_AUTH_TYPE=api_key')
                example_lines.append(f'export {env_prefix}_API_KEY=your_api_key_here')
            elif auth.auth_type == 'custom_header':
                example_lines.append(f'export {env_prefix}_AUTH_TYPE=custom_header')
                example_lines.append(f'export {env_prefix}_CUSTOM_HEADER_NAME={auth.header_name}')
                example_lines.append(f'export {env_prefix}_CUSTOM_HEADER_VALUE=your_value_here')
            break  # Only show first auth pattern as example
        example_lines.append('```')

        return '\n'.join(lines) + '\n'.join(example_lines)

    def _generate_claude_desktop_config(self, env_prefix: str) -> str:
        """Generate Claude Desktop configuration based on discovered auth."""
        auth_patterns = self.service_info.auth_patterns

        if not auth_patterns:
            # No auth - simple config
            return f'''```json
{{
  "mcpServers": {{
    "{self.server_name}": {{
      "command": "uv",
      "args": ["run", "{self.server_name}"],
      "cwd": "/path/to/{self.server_name}"
    }}
  }}
}}
```'''

        # Auth discovered - include env vars
        env_section = ''
        for auth in auth_patterns:
            if auth.auth_type == 'bearer':
                env_section = f''',
      "env": {{
        "{env_prefix}_AUTH_TYPE": "bearer",
        "{env_prefix}_BEARER_TOKEN": "your_token_here"
      }}'''
            elif auth.auth_type == 'api_key':
                env_section = f''',
      "env": {{
        "{env_prefix}_AUTH_TYPE": "api_key",
        "{env_prefix}_API_KEY": "your_api_key_here"
      }}'''
            elif auth.auth_type == 'custom_header':
                env_section = f''',
      "env": {{
        "{env_prefix}_AUTH_TYPE": "custom_header",
        "{env_prefix}_CUSTOM_HEADER_NAME": "{auth.header_name}",
        "{env_prefix}_CUSTOM_HEADER_VALUE": "your_value_here"
      }}'''
            break  # Only use first auth pattern

        return f'''```json
{{
  "mcpServers": {{
    "{self.server_name}": {{
      "command": "uv",
      "args": ["run", "{self.server_name}"],
      "cwd": "/path/to/{self.server_name}"{env_section}
    }}
  }}
}}
```'''

    def _generate_env_example(self, server_dir: str) -> None:
        """Generate .env.example file."""
        env_prefix = self.service_info.name.upper().replace('-', '_').replace('.', '_')
        auth_patterns = self.service_info.auth_patterns

        lines = [
            f'# {self.server_name} Configuration',
            '# Copy this file to .env and update with your values',
            '',
            '# Base URL (optional, defaults to discovered URL)',
            f'# {env_prefix}_BASE_URL={self.service_info.base_url}',
        ]

        if not auth_patterns:
            # No auth discovered
            lines.extend([
                '',
                '# No authentication was detected in the API calls.',
                '# This API appears to be public.',
            ])
        else:
            # Document discovered auth patterns
            for auth in auth_patterns:
                lines.append('')
                if auth.auth_type == 'bearer':
                    lines.append(f'{env_prefix}_AUTH_TYPE=bearer')
                    lines.append(f'{env_prefix}_BEARER_TOKEN=your_token_here')
                elif auth.auth_type == 'api_key':
                    lines.append(f'{env_prefix}_AUTH_TYPE=api_key')
                    lines.append(f'{env_prefix}_API_KEY=your_api_key_here')
                    if auth.header_name and auth.header_name != 'X-API-Key':
                        lines.append(f'{env_prefix}_API_KEY_HEADER={auth.header_name}')
                elif auth.auth_type == 'custom_header':
                    lines.append(f'{env_prefix}_AUTH_TYPE=custom_header')
                    lines.append(f'{env_prefix}_CUSTOM_HEADER_NAME={auth.header_name}')
                    lines.append(f'{env_prefix}_CUSTOM_HEADER_VALUE=your_value_here')

        lines.append('')
        content = '\n'.join(lines)
        self._write_file(server_dir, ".env.example", content)

    def _write_file(self, directory: str, filename: str, content: str) -> None:
        """Write content to a file."""
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def generate_mcp_server(service_info: ServiceInfo, output_dir: str) -> str:
    """
    Generate an MCP server from service information.

    Args:
        service_info: Parsed service information from HAR
        output_dir: Directory to output the generated server

    Returns:
        Path to the generated server directory
    """
    generator = MCPGenerator(service_info, output_dir)
    return generator.generate()


if __name__ == '__main__':
    import sys
    from har_parser import parse_har_file

    if len(sys.argv) < 2:
        print("Usage: python mcp_generator.py <har_file> [output_dir]")
        sys.exit(1)

    har_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    service_info = parse_har_file(har_file)
    server_dir = generate_mcp_server(service_info, output_dir)

    print(f"Generated MCP server at: {server_dir}")
