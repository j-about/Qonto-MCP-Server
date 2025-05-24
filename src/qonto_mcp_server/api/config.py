"""Configuration management for Qonto MCP server.

This module provides comprehensive configuration management for the Qonto MCP server,
supporting both production and development environments with appropriate credential
handling and validation.

The configuration system automatically detects the environment and applies the
appropriate settings, including API endpoints, authentication methods, and
required credentials based on the deployment context.

Environment Support:
    - Production: Uses command-line arguments for secure credential input
    - Development/Staging: Uses environment variables for easy local development

Security Features:
    - No hardcoded credentials or sensitive information
    - Environment-specific credential validation
    - Clear error messages for missing configuration
    - Separate handling of API keys and staging tokens

Dependencies:
    - os: Environment variable access
    - argparse: Command-line argument parsing for production deployment
    - typing: Type hint support for better code safety
"""

import os
import argparse
from typing import Optional


class APIConfig:
    """Configuration manager for Qonto API client credentials and endpoints.

    This class handles all configuration aspects for the Qonto API client,
    including environment detection, credential management, and endpoint
    configuration. It supports both production and development workflows
    with appropriate security measures for each context.

    The configuration automatically adapts based on the ENV environment variable:
    - 'production': Requires API key via command-line argument (--api-key)
    - Other values: Uses environment variables for development convenience

    Attributes:
        env (str): Current environment identifier ('production' or other).
        base_url (str): Base URL for the Qonto API endpoint.
        api_key (str): API key for authentication with Qonto services.
        staging_token (Optional[str]): Additional token required for staging environments.

    Raises:
        ValueError: When required environment variables are missing in non-production mode.
        SystemExit: When required command-line arguments are missing in production mode.

    Example:
        >>> config = APIConfig()  # Automatically detects environment
        >>> print(config.base_url)
        'https://thirdparty.qonto.com/v2'
        >>> print(config.api_key is not None)
        True
    """

    def __init__(self) -> None:
        """Initialize configuration by detecting environment and loading credentials.

        The initialization process follows these steps:
        1. Detect the current environment from ENV variable
        2. Set the appropriate API base URL
        3. Load credentials using the environment-specific method
        4. Validate that all required credentials are available

        For production environments, credentials are loaded from command-line
        arguments to ensure security. For development environments, environment
        variables are used for convenience.

        Raises:
            ValueError: When required environment variables are missing in development mode.
            SystemExit: When required command-line arguments are missing in production mode.
        """
        # Detect environment - defaults to 'production' for security
        self.env = os.getenv("ENV", "production")

        # Configure API endpoint and credentials based on environment
        if self.env == "production":
            # Production environment: use official API endpoint
            self.base_url = "https://thirdparty.qonto.com/v2"

            # Parse command-line arguments for secure credential input
            parser = argparse.ArgumentParser(description="Qonto MCP Server")
            parser.add_argument(
                "--api-key",
                required=True,
                type=str,
                help="Qonto API key for authentication",
            )
            args = parser.parse_args()
            self.api_key = args.api_key

            # Production environments don't use staging tokens
            self.staging_token: Optional[str] = None
        else:
            # Development/staging environment: use sandbox endpoint
            self.base_url = "https://thirdparty-sandbox.staging.qonto.co/v2"

            # Load API key from environment variable
            self.api_key = os.getenv("QONTO_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "QONTO_API_KEY environment variable is required for non-production environments. "
                    "Please set this variable with your Qonto API key."
                )

            # Load staging token (required for sandbox access)
            self.staging_token: Optional[str] = os.getenv("QONTO_STAGING_TOKEN")
            if not self.staging_token:
                raise ValueError(
                    "QONTO_STAGING_TOKEN environment variable is required for non-production environments. "
                    "Please set this variable with your Qonto staging token."
                )
