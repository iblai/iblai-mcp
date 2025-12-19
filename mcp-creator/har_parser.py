"""
HAR File Parser for MCP Server Generation

Parses HTTP Archive (HAR) files to extract API endpoints, request/response patterns,
and authentication mechanisms for generating MCP servers.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse, parse_qs
from collections import defaultdict


@dataclass
class RequestParam:
    """Represents a request parameter (query, path, or body)."""
    name: str
    param_type: str  # 'query', 'path', 'body', 'header'
    example_value: Any = None
    required: bool = False
    description: str = ""


@dataclass
class APIEndpoint:
    """Represents a discovered API endpoint."""
    method: str
    path: str
    base_url: str
    full_url: str
    query_params: list[RequestParam] = field(default_factory=list)
    path_params: list[RequestParam] = field(default_factory=list)
    headers: dict[str, str] = field(default_factory=dict)
    request_body: dict | None = None
    response_example: Any = None
    response_status: int = 200
    content_type: str = "application/json"
    description: str = ""

    @property
    def tool_name(self) -> str:
        """Generate a tool name from the endpoint."""
        # Convert path to snake_case tool name
        path = self.path.strip("/")
        # Replace path params with descriptive names
        path = re.sub(r'\{(\w+)\}', r'\1', path)
        path = re.sub(r'[^a-zA-Z0-9]+', '_', path)
        path = path.strip('_').lower()

        method_prefix = {
            'GET': 'get',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'patch',
            'DELETE': 'delete'
        }.get(self.method.upper(), self.method.lower())

        if path:
            return f"{method_prefix}_{path}"
        return method_prefix


@dataclass
class AuthPattern:
    """Represents an authentication pattern discovered in the HAR."""
    auth_type: str  # 'bearer', 'api_key', 'basic', 'cookie', 'custom_header'
    header_name: str = ""
    example_value: str = ""
    location: str = "header"  # 'header', 'query', 'cookie'


@dataclass
class ServiceInfo:
    """Information about the service extracted from HAR."""
    name: str
    base_url: str
    description: str = ""
    auth_patterns: list[AuthPattern] = field(default_factory=list)
    endpoints: list[APIEndpoint] = field(default_factory=list)


class HARParser:
    """Parses HAR files to extract API patterns for MCP server generation."""

    # Headers to skip (browser-specific, not relevant for API)
    SKIP_HEADERS = {
        'accept-encoding', 'accept-language', 'cache-control', 'pragma',
        'sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform',
        'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site', 'sec-gpc',
        'user-agent', 'upgrade-insecure-requests', 'connection',
        ':method', ':path', ':scheme', ':authority', ':status',
        'priority', 'dnt', 'te', 'if-none-match', 'if-modified-since'
    }

    # Headers that indicate authentication
    AUTH_HEADERS = {
        'authorization': 'bearer',
        'x-api-key': 'api_key',
        'api-key': 'api_key',
        'x-auth-token': 'custom_header',
        'x-access-token': 'custom_header',
    }

    # Static file extensions to skip
    STATIC_EXTENSIONS = {
        '.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
        '.woff', '.woff2', '.ttf', '.eot', '.map', '.webp', '.avif'
    }

    def __init__(self, har_path: str):
        self.har_path = har_path
        self.har_data = None
        self.entries = []

    def load(self) -> None:
        """Load and parse the HAR file."""
        with open(self.har_path, 'r', encoding='utf-8') as f:
            self.har_data = json.load(f)
        self.entries = self.har_data.get('log', {}).get('entries', [])

    def _is_static_resource(self, url: str) -> bool:
        """Check if URL points to a static resource."""
        parsed = urlparse(url)
        path = parsed.path.lower()

        # Check file extensions
        for ext in self.STATIC_EXTENSIONS:
            if path.endswith(ext):
                return True

        # Check common static paths
        static_paths = ['/_next/static', '/static/', '/assets/', '/public/']
        for static_path in static_paths:
            if static_path in path:
                return True

        return False

    def _is_api_call(self, url: str, headers: list[dict]) -> bool:
        """Determine if this is an API call vs page load."""
        parsed = urlparse(url)
        path = parsed.path.lower()

        # Check for explicit API paths
        if '/api/' in path or '/v1/' in path or '/v2/' in path:
            return True

        # Check Accept header
        for header in headers:
            if header.get('name', '').lower() == 'accept':
                value = header.get('value', '').lower()
                if 'application/json' in value:
                    return True

        # Check Content-Type header
        for header in headers:
            if header.get('name', '').lower() == 'content-type':
                value = header.get('value', '').lower()
                if 'application/json' in value:
                    return True

        return False

    def _extract_auth_patterns(self, headers: list[dict]) -> list[AuthPattern]:
        """Extract authentication patterns from headers."""
        patterns = []

        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')

            if name in self.AUTH_HEADERS:
                auth_type = self.AUTH_HEADERS[name]

                # Mask the actual token value
                if value.lower().startswith('bearer '):
                    example_value = 'Bearer <token>'
                else:
                    example_value = '<api_key>'

                patterns.append(AuthPattern(
                    auth_type=auth_type,
                    header_name=header.get('name', ''),  # Keep original case
                    example_value=example_value,
                    location='header'
                ))

        # Check for cookie-based auth
        for header in headers:
            if header.get('name', '').lower() == 'cookie':
                value = header.get('value', '')
                if any(auth_cookie in value.lower() for auth_cookie in
                       ['session', 'auth', 'token', 'jwt']):
                    patterns.append(AuthPattern(
                        auth_type='cookie',
                        header_name='Cookie',
                        example_value='<session_cookie>',
                        location='cookie'
                    ))
                    break

        return patterns

    def _extract_path_params(self, path: str) -> tuple[str, list[RequestParam]]:
        """
        Extract path parameters from URL path.
        Returns normalized path and list of path parameters.
        """
        params = []

        # Common patterns for path parameters (UUIDs, IDs, slugs)
        uuid_pattern = r'/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
        numeric_id_pattern = r'/(\d+)(?=/|$)'

        normalized_path = path

        # Replace UUIDs with parameter placeholder
        uuid_matches = re.finditer(uuid_pattern, path, re.IGNORECASE)
        for i, match in enumerate(uuid_matches):
            param_name = f'uuid_{i}' if i > 0 else 'id'
            normalized_path = normalized_path.replace(
                match.group(0), f'/{{{param_name}}}'
            )
            params.append(RequestParam(
                name=param_name,
                param_type='path',
                example_value=match.group(1),
                required=True,
                description=f'UUID identifier'
            ))

        # Replace numeric IDs
        numeric_matches = list(re.finditer(numeric_id_pattern, normalized_path))
        for i, match in enumerate(numeric_matches):
            param_name = f'id_{i}' if i > 0 else 'id'
            if '{' not in match.group(0):  # Don't replace already parameterized parts
                normalized_path = normalized_path[:match.start()] + \
                    f'/{{{param_name}}}' + normalized_path[match.end():]
                params.append(RequestParam(
                    name=param_name,
                    param_type='path',
                    example_value=match.group(1),
                    required=True,
                    description='Numeric identifier'
                ))

        return normalized_path, params

    def _extract_query_params(self, url: str) -> list[RequestParam]:
        """Extract query parameters from URL."""
        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query)

        params = []
        for name, values in query_dict.items():
            # Skip framework-specific params
            if name.startswith('_') or name in ['rsc', 'callback', 'jsonp']:
                continue

            params.append(RequestParam(
                name=name,
                param_type='query',
                example_value=values[0] if values else None,
                required=False,
                description=f'Query parameter: {name}'
            ))

        return params

    def _extract_request_body(self, request: dict) -> dict | None:
        """Extract request body if present."""
        post_data = request.get('postData', {})
        if not post_data:
            return None

        mime_type = post_data.get('mimeType', '')
        text = post_data.get('text', '')

        if not text:
            return None

        if 'json' in mime_type:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {'raw': text}
        elif 'form' in mime_type:
            params = post_data.get('params', [])
            return {p['name']: p.get('value', '') for p in params}

        return {'raw': text}

    def _extract_response_example(self, response: dict) -> Any:
        """Extract a sample response for documentation."""
        content = response.get('content', {})
        text = content.get('text', '')
        mime_type = content.get('mimeType', '')

        if not text:
            return None

        if 'json' in mime_type:
            try:
                data = json.loads(text)
                # Truncate large responses
                if isinstance(data, dict):
                    return self._truncate_response(data)
                elif isinstance(data, list) and len(data) > 2:
                    return data[:2]  # Keep first 2 items as example
                return data
            except json.JSONDecodeError:
                return None

        return None

    def _truncate_response(self, data: dict, max_depth: int = 3) -> dict:
        """Truncate deep nested structures for examples."""
        if max_depth <= 0:
            return {'...': 'truncated'}

        result = {}
        for key, value in list(data.items())[:10]:  # Max 10 keys
            if isinstance(value, dict):
                result[key] = self._truncate_response(value, max_depth - 1)
            elif isinstance(value, list):
                if len(value) > 2:
                    result[key] = value[:2]
                else:
                    result[key] = value
            else:
                result[key] = value
        return result

    def _normalize_headers(self, headers: list[dict]) -> dict[str, str]:
        """Normalize headers, removing browser-specific ones."""
        result = {}
        for header in headers:
            name = header.get('name', '')
            if name.lower() not in self.SKIP_HEADERS:
                result[name] = header.get('value', '')
        return result

    def _extract_service_name(self) -> str:
        """Extract service name from URLs in the HAR."""
        hosts = set()
        for entry in self.entries:
            url = entry.get('request', {}).get('url', '')
            if url and not self._is_static_resource(url):
                parsed = urlparse(url)
                if parsed.netloc:
                    hosts.add(parsed.netloc)

        if not hosts:
            return 'unknown'

        # Find the primary API host
        for host in hosts:
            if 'api' in host.lower():
                return self._host_to_name(host)

        # Otherwise use the first non-static host
        return self._host_to_name(list(hosts)[0])

    def _host_to_name(self, host: str) -> str:
        """Convert hostname to a service name."""
        # Remove common prefixes/suffixes
        name = host.lower()
        name = re.sub(r'^(www\.|api\.|blog\.)', '', name)
        name = re.sub(r'\.(com|org|net|io|ai|dev)$', '', name)
        name = re.sub(r'[^a-z0-9]+', '-', name)
        return name.strip('-')

    def parse(self) -> ServiceInfo:
        """Parse the HAR file and extract service information."""
        if not self.har_data:
            self.load()

        endpoints_map: dict[str, APIEndpoint] = {}
        all_auth_patterns: list[AuthPattern] = []
        base_urls: set[str] = set()

        for entry in self.entries:
            request = entry.get('request', {})
            response = entry.get('response', {})

            url = request.get('url', '')
            method = request.get('method', 'GET')
            headers = request.get('headers', [])

            # Skip static resources
            if self._is_static_resource(url):
                continue

            # Only process API calls
            if not self._is_api_call(url, headers):
                continue

            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            base_urls.add(base_url)

            # Extract path parameters and normalize path
            normalized_path, path_params = self._extract_path_params(parsed.path)

            # Create unique key for deduplication
            endpoint_key = f"{method}:{base_url}{normalized_path}"

            # Extract auth patterns
            auth_patterns = self._extract_auth_patterns(headers)
            all_auth_patterns.extend(auth_patterns)

            # Extract query params
            query_params = self._extract_query_params(url)

            # Extract request body
            request_body = self._extract_request_body(request)

            # Extract response example
            response_example = self._extract_response_example(response)

            # Normalize headers
            normalized_headers = self._normalize_headers(headers)

            endpoint = APIEndpoint(
                method=method,
                path=normalized_path,
                base_url=base_url,
                full_url=url,
                query_params=query_params,
                path_params=path_params,
                headers=normalized_headers,
                request_body=request_body,
                response_example=response_example,
                response_status=response.get('status', 200),
                content_type=normalized_headers.get('Content-Type', 'application/json')
            )

            # Deduplicate - keep the one with more information
            if endpoint_key in endpoints_map:
                existing = endpoints_map[endpoint_key]
                # Merge query params
                existing_param_names = {p.name for p in existing.query_params}
                for param in query_params:
                    if param.name not in existing_param_names:
                        existing.query_params.append(param)
            else:
                endpoints_map[endpoint_key] = endpoint

        # Deduplicate auth patterns
        unique_auth = {}
        for pattern in all_auth_patterns:
            key = f"{pattern.auth_type}:{pattern.header_name}"
            if key not in unique_auth:
                unique_auth[key] = pattern

        service_name = self._extract_service_name()
        primary_base_url = list(base_urls)[0] if base_urls else ''

        return ServiceInfo(
            name=service_name,
            base_url=primary_base_url,
            description=f"API service for {service_name}",
            auth_patterns=list(unique_auth.values()),
            endpoints=list(endpoints_map.values())
        )


def parse_har_file(har_path: str) -> ServiceInfo:
    """Convenience function to parse a HAR file."""
    parser = HARParser(har_path)
    return parser.parse()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python har_parser.py <har_file>")
        sys.exit(1)

    service_info = parse_har_file(sys.argv[1])

    print(f"\nService: {service_info.name}")
    print(f"Base URL: {service_info.base_url}")
    print(f"\nAuth Patterns: {len(service_info.auth_patterns)}")
    for auth in service_info.auth_patterns:
        print(f"  - {auth.auth_type}: {auth.header_name}")

    print(f"\nEndpoints: {len(service_info.endpoints)}")
    for endpoint in service_info.endpoints:
        print(f"  - {endpoint.method} {endpoint.path} -> {endpoint.tool_name}")
        if endpoint.query_params:
            print(f"    Query params: {[p.name for p in endpoint.query_params]}")
