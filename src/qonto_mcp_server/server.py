"""Qonto MCP Server implementation.

This module contains the core MCP server implementation for the Qonto banking API.
It provides automatic tool registration using runtime introspection to dynamically
discover and register all public async methods from the APIMethods class as MCP tools.

The server uses FastMCP as the underlying MCP implementation and automatically
handles parameter mapping, type preservation, and tool registration without
requiring manual configuration for each API endpoint.

Key Features:
    - Automatic tool discovery and registration via introspection
    - Type-safe parameter handling with preserved signatures
    - Dynamic wrapper function generation for seamless MCP integration
    - Comprehensive error handling and API client management

Dependencies:
    - mcp.server.fastmcp: Core MCP server implementation
    - .api.config: Configuration management for API credentials and API base URL
    - .api.client: HTTP client for Qonto API interactions
    - .api.methods: Collection of all Qonto API method implementations
"""

import asyncio
import functools
import inspect
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from .api.config import APIConfig
from .api.client import APIClient
from .api.methods import APIMethods


def _register_tool_from_method(
    mcp: FastMCP, api_methods: APIMethods, method_name: str
) -> None:
    """Register a single API method as an MCP tool using runtime introspection.

    This function performs dynamic tool registration by extracting method signatures,
    preserving type annotations, and creating MCP-compatible wrapper functions.
    It eliminates the need for manual parameter definition duplication while
    maintaining full type safety and documentation preservation.

    The registration process involves:
    1. Extracting the original method's signature and documentation
    2. Creating a new signature excluding the 'self' parameter
    3. Generating a dynamic wrapper function with preserved metadata
    4. Registering the wrapper as an MCP tool

    Args:
        mcp (FastMCP): The FastMCP server instance for tool registration.
        api_methods (APIMethods): The APIMethods instance containing the target method.
        method_name (str): The name of the method to register as an MCP tool.
            This name will be used as the tool identifier in MCP.

    Returns:
        None

    Note:
        The wrapper function automatically converts all parameters to keyword-only
        to ensure compatibility with MCP's parameter passing mechanism.
    """
    # Extract the target method and its introspection data
    method = getattr(api_methods, method_name)
    signature = inspect.signature(method)
    doc = inspect.getdoc(method)

    # Build parameter list for the wrapper function, excluding 'self'
    # Convert all parameters to keyword-only for MCP compatibility
    params = []
    for param_name, param in signature.parameters.items():
        if param_name == "self":
            continue  # Skip 'self' parameter as it's not needed in the wrapper
        params.append(param.replace(kind=inspect.Parameter.KEYWORD_ONLY))

    # Create new signature for the wrapper function with filtered parameters
    wrapper_signature = signature.replace(parameters=params)

    # Define the dynamic wrapper function that will be registered as an MCP tool
    async def tool_wrapper(**kwargs: Any) -> Dict[str, Any]:
        """Dynamically created wrapper function that calls the original API method.

        This wrapper preserves the original method's signature while adapting it
        for MCP tool registration. All arguments are passed through to the
        original method unchanged.

        Args:
            **kwargs: Keyword arguments passed from the MCP client.

        Returns:
            Dict[str, Any]: The response from the original API method.
        """
        return await method(**kwargs)

    # Preserve the original method's metadata in the wrapper function
    tool_wrapper.__signature__ = wrapper_signature  # type: ignore
    tool_wrapper.__doc__ = doc
    tool_wrapper.__name__ = method_name
    tool_wrapper = functools.wraps(method)(tool_wrapper)

    # Register the wrapper function as an MCP tool
    mcp.tool(name=method_name, description=doc or "")(tool_wrapper)


def _register_all_tools(mcp: FastMCP, api_methods: APIMethods) -> None:
    """Automatically discover and register all public async methods as MCP tools.

    This function performs bulk tool registration by using runtime introspection
    to discover all eligible methods in the APIMethods class. It filters methods
    based on specific criteria to ensure only appropriate API methods are registered.

    Method Selection Criteria:
    - Must be a bound method (not a function or property)
    - Must not start with underscore (excludes private/protected methods)
    - Must be an async coroutine function (required for MCP tool compatibility)

    This approach eliminates the need for manual tool registration and automatically
    adapts to new methods added to the APIMethods class, reducing maintenance overhead
    and preventing registration inconsistencies.

    Args:
        mcp (FastMCP): The FastMCP server instance for tool registration.
        api_methods (APIMethods): The APIMethods instance containing methods to register.
            All qualifying public async methods will be registered as MCP tools.

    Returns:
        None

    Note:
        This function delegates the actual registration of each individual method
        to _register_tool_from_method() for consistency and maintainability.
    """
    # Use introspection to discover all qualifying methods
    # The predicate function filters methods based on our registration criteria
    methods = inspect.getmembers(
        api_methods,
        predicate=lambda x: (
            inspect.ismethod(x)  # Must be a bound method
            and not x.__name__.startswith("_")  # Exclude private/protected methods
            and asyncio.iscoroutinefunction(x)  # Must be async for MCP compatibility
        ),
    )

    # Register each discovered method as an MCP tool
    for method_name, _ in methods:
        _register_tool_from_method(mcp, api_methods, method_name)


def create_server() -> FastMCP:
    """Initialize and configure the complete MCP server with all dependencies.

    This function orchestrates the creation of the entire MCP server infrastructure
    by instantiating all required components and configuring automatic tool registration.

    Component Initialization Order:
    1. APIConfig: Loads configuration from environment variables and command line
    2. APIClient: Creates HTTP client with proper authentication headers
    3. APIMethods: Instantiates the collection of all Qonto API methods
    4. FastMCP: Creates the MCP server instance with the specified name
    5. Tool Registration: Automatically discovers and registers all API methods

    Returns:
        FastMCP: A fully configured MCP server instance ready to handle client requests.
            All Qonto API methods are registered as tools and ready for use.

    Note:
        This function uses a factory pattern to encapsulate the complex initialization
        process and ensure proper dependency injection between components.
    """
    # Initialize configuration management (handles environment variables and CLI args)
    api_config = APIConfig()

    # Create HTTP client with authentication and request handling
    api_client = APIClient(api_config)

    # Instantiate the collection of all Qonto API method implementations
    api_methods = APIMethods(api_client)

    # Create the FastMCP server instance with a descriptive name
    mcp = FastMCP("Qonto MCP Server")

    # Automatically discover and register all API methods as MCP tools
    _register_all_tools(mcp, api_methods)

    return mcp


# Module-level server instance created once during import
# This follows the singleton pattern for the MCP server
mcp = create_server()


def serve() -> None:
    """Launch the MCP server and start processing client requests.

    This function serves as the final entry point that actually starts the server
    execution loop. It delegates to the FastMCP server's run() method which handles
    all the low-level MCP protocol communication, request routing, and response
    generation.

    The server will run indefinitely until interrupted by the user (Ctrl+C) or
    terminated by the process manager. All registered tools become available
    immediately upon server startup.

    Returns:
        None

    Note:
        This function is blocking and will not return until the server is shut down.
        It's designed to be called from command-line interfaces or application launchers.
    """
    mcp.run()
