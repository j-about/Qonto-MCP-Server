"""Qonto API client module.

This module provides the complete API client implementation for the Qonto banking API.
It includes configuration management, HTTP client functionality, and comprehensive
method implementations for all supported Qonto API endpoints.

The module is organized into three main components:

1. Configuration Management (config.py):
   - Environment-based configuration loading
   - Command-line argument parsing for production use
   - Support for both production and staging environments
   - Secure credential handling

2. HTTP Client (client.py):
   - Async HTTP client built on httpx
   - Automatic authentication header management
   - Comprehensive error handling and retry logic
   - Support for various HTTP methods and content types

3. API Methods (methods.py):
   - Complete implementation of all Qonto API endpoints
   - Type-safe method signatures with comprehensive documentation
   - Structured parameter handling and validation
   - Standardized response formatting

The module follows strict Python conventions including PEP 8 style guidelines,
PEP 257 docstring standards, and PEP 484 type annotations throughout.

Key Features:
    - Full async/await support for non-blocking operations
    - Comprehensive type hints for better IDE support and runtime safety
    - Detailed docstrings following Google/Sphinx documentation standards
    - Modular design for easy testing and maintenance
    - Environment-specific configuration management
    - Robust error handling and logging capabilities

Usage:
    The module is typically used through the MCP server implementation:

    >>> from qonto_mcp_server.api.config import APIConfig
    >>> from qonto_mcp_server.api.client import APIClient
    >>> from qonto_mcp_server.api.methods import APIMethods
    >>>
    >>> config = APIConfig()
    >>> client = APIClient(config)
    >>> methods = APIMethods(client)

Dependencies:
    - httpx: Modern async HTTP client library
    - typing: Type hint support for Python < 3.9
    - argparse: Command-line argument parsing
    - os: Environment variable access
    - pathlib: Path manipulation utilities
    - json: JSON encoding/decoding for API payloads
"""
