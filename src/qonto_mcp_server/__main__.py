"""Entry point for running qonto_mcp_server as a module with uvx (python -m).

This module enables the package to be executed directly using Python's -m flag,
providing compatibility with package managers like uv and standard Python
module execution patterns.

Example usage:
    uvx qonto_mcp_server --api-key API_LOGIN:API_SECRET_KEY
    python -m qonto_mcp_server --api-key API_LOGIN:API_SECRET_KEY

The module delegates execution to the main() function defined in the package's
__init__.py file, which in turn starts the MCP server.
"""

from qonto_mcp_server import main

# Module execution guard - ensures this code only runs when the module
# is executed directly, not when imported
if __name__ == "__main__":
    main()
