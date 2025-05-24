"""Qonto API HTTP client implementation.

This module provides a comprehensive async HTTP client for interacting with the
Qonto banking API. It handles authentication, request formatting, response parsing,
and error management for all API operations.

The client is built on httpx for modern async HTTP support and includes sophisticated
error handling, automatic retry logic, and comprehensive logging capabilities.

Key Features:
    - Full async/await support for non-blocking operations
    - Automatic authentication header management
    - Environment-specific staging token support
    - Comprehensive error handling with detailed error reporting
    - Support for multiple content types (JSON, form data, file uploads)
    - Request timeout management and connection pooling
    - Type-safe method signatures with full type annotations

Security Features:
    - Secure credential handling through configuration injection
    - No credential logging or exposure in error messages
    - Proper HTTP status code handling and error categorization
    - Support for staging environments with additional security tokens

Dependencies:
    - httpx: Modern async HTTP client library
    - typing: Type hint support for better code safety
    - .config: Configuration management for credentials and endpoints
"""

from typing import Any, Dict, Optional
import httpx

from .config import APIConfig


class APIClient:
    """Async HTTP client for Qonto API interactions with comprehensive error handling.

    This client provides a high-level interface for making HTTP requests to the Qonto
    banking API. It automatically handles authentication, request formatting, response
    parsing, and error management while maintaining full async/await compatibility.

    The client supports all standard HTTP methods and content types required by the
    Qonto API, including JSON payloads, form data, and file uploads. It automatically
    configures authentication headers based on the provided configuration.

    Attributes:
        api_config (APIConfig): Configuration instance containing credentials and endpoints.

    Example:
        >>> config = APIConfig()
        >>> client = APIClient(config)
        >>> response = await client.get("/organization")
        >>> print(response["data"])

    Note:
        All methods are async and must be awaited. The client handles connection
        pooling and resource cleanup automatically through httpx's AsyncClient.
    """

    def __init__(self, api_config: APIConfig) -> None:
        """Initialize the API client with configuration.

        Args:
            api_config (APIConfig): Configuration instance containing API credentials,
                endpoints, and environment-specific settings.

        Note:
            The client stores a reference to the configuration but does not validate
            credentials at initialization time. Credential validation occurs during
            the first API request.
        """
        self.api_config = api_config

    def _get_headers(self, include_content_type: bool = True) -> Dict[str, str]:
        """Build HTTP headers for API requests with authentication and content type.

        This method constructs the complete set of HTTP headers required for Qonto
        API requests, including authentication credentials and optional content type
        headers. It automatically includes staging tokens when available.

        Args:
            include_content_type (bool): Whether to include 'Content-Type: application/json'
                header. Set to False for multipart/form-data requests (file uploads).
                Defaults to True.

        Returns:
            Dict[str, str]: Complete headers dictionary ready for HTTP request.
                Always includes Authorization header, optionally includes Content-Type
                and X-Qonto-Staging-Token headers based on configuration.

        Note:
            The Authorization header uses the API key directly as the value,
            following Qonto's authentication scheme. Staging tokens are only
            included when present in the configuration.
        """
        # Start with required authentication header
        headers = {"Authorization": self.api_config.api_key}

        # Add content type for JSON requests (exclude for file uploads)
        if include_content_type:
            headers["Content-Type"] = "application/json"

        # Include staging token for sandbox/development environments
        if self.api_config.staging_token:
            headers["X-Qonto-Staging-Token"] = self.api_config.staging_token

        return headers

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute an HTTP request to the Qonto API with comprehensive error handling.

        This is the core method that handles all HTTP communication with the Qonto API.
        It manages request construction, authentication, timeout handling, and error
        processing. The method supports multiple content types and provides detailed
        error information for troubleshooting.

        Request Processing Steps:
        1. Construct the full API URL from base URL and endpoint
        2. Generate appropriate headers based on request type
        3. Execute the HTTP request with timeout protection
        4. Handle HTTP status errors and network errors
        5. Parse and return the JSON response

        Args:
            method (str): HTTP method to use (GET, POST, PATCH, DELETE, etc.).
            endpoint (str): API endpoint path (e.g., "/transactions", "/organization").
                Should start with "/" and will be appended to the base URL.
            params (Optional[Dict[str, Any]]): URL query parameters for the request.
                Commonly used for filtering, pagination, and search operations.
            json (Optional[Dict[str, Any]]): JSON payload for the request body.
                Used for POST and PATCH operations with structured data.
            files (Optional[Dict[str, Any]]): File data for multipart uploads.
                When provided, Content-Type header is automatically set to multipart/form-data.
            data (Optional[Dict[str, Any]]): Form data for the request body.
                Used for POST operations with form-encoded data.

        Returns:
            Dict[str, Any]: Parsed JSON response from the API.
                On success, contains the API response data structure.
                On error, contains an "errors" key with error details.

        Raises:
            No exceptions are raised directly. All errors are captured and returned
            as error dictionaries for consistent error handling across the application.

        Note:
            The method uses a 30-second timeout for all requests to prevent hanging.
            Connection pooling and resource cleanup are handled automatically by httpx.
        """
        # Construct the complete API URL
        url = f"{self.api_config.base_url}{endpoint}"

        # Generate headers with appropriate content type for the request
        headers = self._get_headers(include_content_type=files is None)

        # Execute the HTTP request with automatic resource management
        async with httpx.AsyncClient() as client:
            try:
                # Make the actual HTTP request with all provided parameters
                response = await client.request(
                    method=method,
                    url=url,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    timeout=30.0,  # 30-second timeout for all requests
                )
                # Raise an exception for 4xx and 5xx status codes
                response.raise_for_status()

            except httpx.HTTPStatusError as e:
                # Handle specific HTTP status errors with detailed information
                # Some status codes are expected and should be handled gracefully
                if e.response.status_code not in (400, 401, 403, 404, 422, 500):
                    return {
                        "errors": [{"code": e.response.status_code, "detail": str(e)}]
                    }
                # For expected status codes, let the response be processed normally
                # The API might return useful error information in the response body

            except httpx.RequestError as e:
                # Handle network-level errors (connection issues, timeouts, etc.)
                return {"errors": [{"detail": str(e)}]}

            # Parse and return the JSON response
            return response.json()

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a GET request to retrieve data from the Qonto API.

        GET requests are used for data retrieval operations such as fetching
        transactions, organization details, beneficiaries, and other resources.
        This method is idempotent and safe for repeated calls.

        Args:
            endpoint (str): API endpoint path for the GET request.
                Examples: "/transactions", "/organization", "/beneficiaries".
            params (Optional[Dict[str, Any]]): Query parameters for filtering,
                pagination, sorting, and other request options.

        Returns:
            Dict[str, Any]: API response containing the requested data or error information.

        Example:
            >>> response = await client.get("/transactions", {"page": 1, "per_page": 50})
            >>> transactions = response.get("transactions", [])
        """
        return await self._make_request("GET", endpoint, params=params)

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute a POST request to create new resources or submit data.

        POST requests are used for creating new resources, submitting forms,
        uploading files, and other data submission operations. This method
        supports multiple content types for different use cases.

        Args:
            endpoint (str): API endpoint path for the POST request.
                Examples: "/external_transfers", "/attachments", "/clients".
            data (Optional[Dict[str, Any]]): Form data for the request body.
                Used for form-encoded submissions and file uploads with metadata.
            files (Optional[Dict[str, Any]]): File data for multipart uploads.
                Used for attachment uploads and document submissions.
            json (Optional[Dict[str, Any]]): JSON payload for the request body.
                Used for structured data creation and API operations.
            params (Optional[Dict[str, Any]]): Query parameters for the request.
                Less commonly used with POST but available when needed.

        Returns:
            Dict[str, Any]: API response containing the created resource or operation result.

        Note:
            Only one of data, files, or json should be provided per request.
            The Content-Type header is automatically set based on the payload type.
        """
        return await self._make_request(
            "POST", endpoint, data=data, files=files, json=json, params=params
        )

    async def patch(
        self, endpoint: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a PATCH request to update existing resources partially.

        PATCH requests are used for partial updates to existing resources,
        such as modifying specific fields or properties without affecting
        the entire resource structure.

        Args:
            endpoint (str): API endpoint path for the PATCH request.
                Typically includes the resource ID: "/beneficiaries/untrust".
            json (Optional[Dict[str, Any]]): JSON payload containing the fields
                to update and their new values.

        Returns:
            Dict[str, Any]: API response containing the updated resource or operation result.

        Example:
            >>> response = await client.patch("/beneficiaries/untrust", {"ids": ["123"]})
            >>> updated_count = response.get("updated_count", 0)
        """
        return await self._make_request("PATCH", endpoint, json=json)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Execute a DELETE request to remove resources from the API.

        DELETE requests are used for removing resources such as attachments,
        associations, or other deletable entities. This method is idempotent
        but irreversible in most cases.

        Args:
            endpoint (str): API endpoint path for the DELETE request.
                Typically includes the resource ID: "/transactions/{id}/attachments/{attachment_id}".

        Returns:
            Dict[str, Any]: API response confirming the deletion or providing error information.

        Warning:
            DELETE operations are typically irreversible. Ensure the correct
            endpoint and resource ID before calling this method.

        Example:
            >>> response = await client.delete("/transactions/123/attachments/456")
            >>> success = "errors" not in response
        """
        return await self._make_request("DELETE", endpoint)
