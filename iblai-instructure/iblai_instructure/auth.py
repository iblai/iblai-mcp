"""
Authentication Manager for iblai-instructure

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
        auth_type_str = os.getenv("INSTRUCTURE_AUTH_TYPE", "none").lower()

        try:
            auth_type = AuthType(auth_type_str)
        except ValueError:
            auth_type = AuthType.NONE

        return AuthConfig(
            auth_type=auth_type,
            api_key=os.getenv("INSTRUCTURE_API_KEY"),
            api_key_header=os.getenv("INSTRUCTURE_API_KEY_HEADER", "X-API-Key"),
            bearer_token=os.getenv("INSTRUCTURE_BEARER_TOKEN"),
            basic_username=os.getenv("INSTRUCTURE_BASIC_USERNAME"),
            basic_password=os.getenv("INSTRUCTURE_BASIC_PASSWORD"),
            custom_header_name=os.getenv("INSTRUCTURE_CUSTOM_HEADER_NAME"),
            custom_header_value=os.getenv("INSTRUCTURE_CUSTOM_HEADER_VALUE"),
            oauth2_client_id=os.getenv("INSTRUCTURE_OAUTH2_CLIENT_ID"),
            oauth2_client_secret=os.getenv("INSTRUCTURE_OAUTH2_CLIENT_SECRET"),
            oauth2_token_url=os.getenv("INSTRUCTURE_OAUTH2_TOKEN_URL"),
            oauth2_scope=os.getenv("INSTRUCTURE_OAUTH2_SCOPE"),
        )

    def get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers based on current configuration."""
        if self.config.auth_type == AuthType.NONE:
            return {}

        elif self.config.auth_type == AuthType.API_KEY:
            if self.config.api_key:
                return {self.config.api_key_header: self.config.api_key}
            return {}

        elif self.config.auth_type == AuthType.BEARER:
            if self.config.bearer_token:
                return {"Authorization": f"Bearer {self.config.bearer_token}"}
            return {}

        elif self.config.auth_type == AuthType.BASIC:
            if self.config.basic_username and self.config.basic_password:
                credentials = f"{self.config.basic_username}:{self.config.basic_password}"
                encoded = base64.b64encode(credentials.encode()).decode()
                return {"Authorization": f"Basic {encoded}"}
            return {}

        elif self.config.auth_type == AuthType.CUSTOM_HEADER:
            if self.config.custom_header_name and self.config.custom_header_value:
                return {self.config.custom_header_name: self.config.custom_header_value}
            return {}

        elif self.config.auth_type == AuthType.OAUTH2_CLIENT_CREDENTIALS:
            token = self._get_oauth2_token()
            if token:
                return {"Authorization": f"Bearer {token}"}
            return {}

        return {}

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

            data = {
                "grant_type": "client_credentials",
                "client_id": self.config.oauth2_client_id,
                "client_secret": self.config.oauth2_client_secret,
            }

            if self.config.oauth2_scope:
                data["scope"] = self.config.oauth2_scope

            with httpx.Client() as client:
                response = client.post(
                    self.config.oauth2_token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()

                token_data = response.json()
                self._oauth2_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)
                self._token_expiry = time.time() + expires_in

                return self._oauth2_token

        except Exception as e:
            print(f"OAuth2 token fetch failed: {e}")
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
