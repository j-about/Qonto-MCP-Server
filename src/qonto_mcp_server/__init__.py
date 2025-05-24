"""Qonto MCP Server package.

This package provides a Model Context Protocol (MCP) server for the Qonto banking API.
The server exposes Qonto's REST API functionality as MCP tools, enabling integration
with MCP-compatible clients to perform banking operations such as retrieving transactions,
managing beneficiaries, handling invoices, and more.

The package follows PEP 8 coding standards and includes comprehensive type hints
throughout the codebase for better code reliability and IDE support.
"""

from .server import serve


def main() -> None:
    """Initialize and start the Qonto MCP server.

    This function serves as the primary entry point for the application.
    It delegates to the serve() function which configures and starts
    the FastMCP server with all registered Qonto API tools.

    The server automatically discovers and registers all public async methods
    from the APIMethods class as MCP tools using runtime introspection.

    Returns:
        None

    Note:
        This function is designed to be called from command line interfaces
        or package managers like uvx.
    """
    serve()


# Module-level execution guard for direct script execution
if __name__ == "__main__":
    main()
