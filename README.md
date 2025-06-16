# Qonto-MCP-Server

MCP Server for the Qonto API.

## Supported API Methods

This MCP server supports all endpoints of Qonto's Business API that are accessible via API key authentication. For a comprehensive list of these endpoints, please refer to the official Qonto documentation:

👉 [Endpoints accessible with an API key](https://docs.qonto.com/api-reference/business-api/authentication/introduction#endpoints-access)

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run _qonto-mcp-server_.

### Using PIP

Alternatively you can install `qonto-mcp-server` via pip:

```
pip install qonto-mcp-server
```

## Configuration

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

- Note: For details on how to obtain `API_LOGIN` and `API_SECRET_KEY` values, see the [Qonto API key docs](https://docs.qonto.com/api-reference/business-api/authentication/api-key).

#### Using uvx

```json
"mcpServers": {
  "qonto-mcp-server": {
    "command": "uvx",
    "args": ["qonto-mcp-server", "--api-key", "API_LOGIN:API_SECRET_KEY"]
  }
}
```

#### Using pip installation

```json
"mcpServers": {
  "qonto-mcp-server": {
    "command": "python",
    "args": ["-m", "qonto-mcp-server", "--api-key", "API_LOGIN:API_SECRET_KEY"]
  }
}
```
