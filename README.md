# Qonto-MCP-Server

MCP Server for the Qonto API.

## Supported API methods

<div style="display: flex; gap: 20px;">
    <table>
        <thead>
            <tr>
                <th>Endpoint</th>
                <th>Supported</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><em>External transfers</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>Retrieve an external transfer</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>List external transfers</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Beneficiaries</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List beneficiaries</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Retrieve a beneficiary</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Untrust a list of beneficiaries</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><em>SEPA Beneficiaries</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List SEPA beneficiaries</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Retrieve a SEPA beneficiary</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Attachments</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>Upload an attachment</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><strong>Retrieve an attachment</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Labels</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List labels</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Retrieve a label</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Memberships</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List memberships</strong></td>
                <td>✅</td>
            </tr>
        </tbody>
    </table>
    <table>
        <thead>
            <tr>
                <th>Endpoint</th>
                <th>Supported</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><em>Organization</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>Retrieve the authenticated organization and list bank accounts</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Attachments in transactions</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List attachments for a transaction</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Upload an attachment to a transaction</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><strong>Remove all attachments from a transaction</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><strong>Remove an attachment from a transaction</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><em>Transactions</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List transactions</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Retrieve a transaction</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Internal transfers</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>Create an internal transfer</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><em>Requests</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List requests</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Supplier invoices</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>Retrieve a supplier invoice</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>List supplier invoices</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Create supplier invoices</strong></td>
                <td>❌</td>
            </tr>
        </tbody>
    </table>
    <table>
        <thead>
            <tr>
                <th>Endpoint</th>
                <th>Supported</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><em>Client invoices</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List client invoices</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Create a client invoice</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><strong>Retrieve a client invoice</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Credit notes</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List credit notes</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Retrieve a credit note</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Clients</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>Retrieve a client</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>List clients</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Create a client</strong></td>
                <td>❌</td>
            </tr>
            <tr>
                <td><em>Statements</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>Retrieve a statement</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>List statements</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><em>Business Accounts</em></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>List business accounts</strong></td>
                <td>✅</td>
            </tr>
            <tr>
                <td><strong>Retrieve a business account</strong></td>
                <td>✅</td>
            </tr>
        </tbody>
    </table>
</div>

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

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "qonto-mcp-server": {
    "command": "uvx",
    "args": ["qonto-mcp-server", "--api-key", "API_LOGIN:API_SECRET_KEY"]
  }
}
```

</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "git": {
    "command": "python",
    "args": ["-m", "qonto-mcp-server", "--api-key", "API_LOGIN:API_SECRET_KEY"]
  }
}
```

</details>
