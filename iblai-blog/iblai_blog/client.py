"""
API Client for iblai-blog

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
        super().__init__(f"API Error {status_code}: {message}")


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
        url = f"{self.base_url}{path}"
        if query_params:
            # Filter out None values
            filtered_params = {k: v for k, v in query_params.items() if v is not None}
            if filtered_params:
                url = f"{url}?{urlencode(filtered_params)}"

        # Build headers
        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

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
                    message=f"Request failed: {response.status_code}",
                    response_body=error_body
                )

            # Parse response
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return {"text": response.text, "status_code": response.status_code}

        except httpx.TimeoutException as e:
            raise APIError(
                status_code=408,
                message=f"Request timed out: {str(e)}"
            )
        except httpx.RequestError as e:
            raise APIError(
                status_code=0,
                message=f"Request failed: {str(e)}"
            )

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
