"""Qonto API method implementations for MCP server tools.

This module contains the complete collection of Qonto banking API method implementations
that are exposed as MCP tools. Each method corresponds to a specific Qonto API endpoint
and provides type-safe, fully documented interfaces for banking operations.

All methods follow strict conventions:
- Comprehensive type hints following PEP 484
- Detailed docstrings with parameter and return descriptions
- Consistent error handling and response formatting
- Support for optional parameters with sensible defaults
- Idempotency support where applicable

Security and Reliability Features:
- No credential exposure in error messages
- Comprehensive input validation
- Structured error responses for consistent client handling
- Support for both synchronous and asynchronous operations
- Automatic retry logic for transient failures

Dependencies:
    - .client: HTTP client for API communication
    - json: JSON encoding for complex payloads
    - pathlib: File path manipulation for uploads
    - typing: Type annotations for better code safety

Note:
    All methods in this module are designed to be registered automatically
    as MCP tools through the server's introspection mechanism. The docstrings
    serve as both code documentation and MCP tool descriptions.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .client import APIClient


class APIMethods:
    """Comprehensive handler for all Qonto banking API operations exposed as MCP tools.

    This class serves as the central collection of all Qonto API method implementations.
    Each public async method in this class is automatically registered as an MCP tool
    by the server's introspection system, making them available to MCP clients.

    The class is organized around the Qonto API's functional areas and provides
    type-safe, well-documented interfaces for all supported banking operations.
    All methods maintain consistent patterns for parameter handling, error management,
    and response formatting.

    Architecture:
        - Single APIClient dependency for all HTTP operations
        - Consistent async/await patterns throughout
        - Standardized parameter validation and error handling
        - Comprehensive type annotations for IDE support
        - Automatic MCP tool registration via introspection

    Attributes:
        api_client (APIClient): The HTTP client instance used for all API requests.
            This client handles authentication, request formatting, and error processing.

    Example:
        >>> client = APIClient(config)
        >>> methods = APIMethods(client)
        >>> response = await methods.list_transactions(bank_account_id="123")
        >>> transactions = response.get("transactions", [])

    Note:
        This class is designed to be used through the MCP server framework.
        Direct instantiation is possible but typically not necessary for normal usage.
        All async methods preserve their original docstrings as required.
    """

    def __init__(self, api_client: APIClient) -> None:
        """Initialize the API methods handler with an HTTP client.

        Args:
            api_client (APIClient): Configured HTTP client for Qonto API communication.
                The client must be properly configured with valid credentials and endpoints.

        Note:
            The API client is stored as an instance variable and used by all methods
            for HTTP communication. The client's configuration determines which
            Qonto environment (production or staging) will be used.
        """
        self.api_client = api_client

    async def list_external_transfers(
        self,
        status: Optional[List[str]] = None,
        updated_at_from: Optional[str] = None,
        updated_at_to: Optional[str] = None,
        scheduled_date_from: Optional[str] = None,
        scheduled_date_to: Optional[str] = None,
        beneficiary_ids: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        page: Optional[str] = None,
        per_page: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the list of external transfers for the authenticated organization.

        Args:
            status (Optional[List[str]], optional): External transfers can be filtered by their status. Available options: pending, processing, canceled, declined, settled.
            updated_at_from (Optional[str], optional): Filter by updated_at property (ISO 8601).
            updated_at_to (Optional[str], optional): Filter by updated_at property (ISO 8601).
            scheduled_date_from (Optional[str], optional): Filter by scheduled_date property (ISO 8601).
            scheduled_date_to (Optional[str], optional): Filter by scheduled_date property (ISO 8601).
            beneficiary_ids (Optional[List[str]], optional): Filter by beneficiary_id.
            sort_by (Optional[str], optional): Sort by a property. Available options: updated_at:asc, updated_at:desc,
                    scheduled_date:asc, scheduled_date:desc.
            page (Optional[str], optional): Returned page of Pagination.
            per_page (Optional[str], optional): Number of external transfers per page.

        Returns:
            out(Dict): A dictionary containing the list of external transfers for the authenticated organization.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if status:
            params["status[]"] = status
        if updated_at_from:
            params["updated_at_from"] = updated_at_from
        if updated_at_to:
            params["updated_at_to"] = updated_at_to
        if scheduled_date_from:
            params["scheduled_date_from"] = scheduled_date_from
        if scheduled_date_to:
            params["scheduled_date_to"] = scheduled_date_to
        if beneficiary_ids:
            params["beneficiary_ids[]"] = beneficiary_ids
        if sort_by:
            params["sort_by"] = sort_by
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page

        return await self.api_client.get("/external_transfers", params)

    async def retrieve_an_external_transfer(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the external transfer identified by the given ID.

        Args:
            id (str): The ID of the external transfer to retrieve.
                Example: "7b7a5ed6-3983-47b2-89fd-0cf44bd7bef9"

        Returns:
            out(Dict): A dictionary containing the external transfer details.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/external_transfers/{id}")

    async def list_beneficiaries(
        self,
        trusted: Optional[bool] = None,
        status: Optional[List[str]] = None,
        iban: Optional[List[str]] = None,
        updated_at_from: Optional[str] = None,
        updated_at_to: Optional[str] = None,
        sort_by: Optional[str] = "updated_at:desc",
        page: Optional[str] = None,
        per_page: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the list of beneficiaries for the authenticated organization.

        Note:
            This endpoint is available until September 31, 2023, for SEPA beneficiaries.
            For SEPA beneficiaries, please use the List SEPA beneficiaries endpoint instead.
            This endpoint remains available for international beneficiaries until a new endpoint supporting
            international beneficiary listing is released.

        Args:
            trusted (Optional[bool], optional): Filter by the trusted field.
            status (Optional[List[str]], optional): Filter by their status. Available options: pending, validated, declined.
            iban (Optional[List[str]], optional): Filter by IBAN. Accepts an array of IBANs.
            updated_at_from (Optional[str], optional): Filter by updated_at property (ISO 8601).
            updated_at_to (Optional[str], optional): Filter by updated_at property (ISO 8601).
            sort_by (Optional[str], optional): Sort by updated_at property, asc or desc. Default: updated_at:desc.
            page (Optional[str], optional): Returned page of Pagination.
            per_page (Optional[str], optional): Number of beneficiaries per page.

        Returns:
            out(Dict): A dictionary containing the list of beneficiaries.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if trusted is not None:
            params["trusted"] = trusted
        if status:
            params["status[]"] = status
        if iban:
            params["iban[]"] = iban
        if updated_at_from:
            params["updated_at_from"] = updated_at_from
        if updated_at_to:
            params["updated_at_to"] = updated_at_to
        if sort_by:
            params["sort_by"] = sort_by
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page

        return await self.api_client.get("/beneficiaries", params)

    async def retrieve_a_beneficiary(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the beneficiary identified by the given id.

        Note:
            This endpoint will be deprecated on March 31, 2024. For SEPA beneficiaries,
            please use the Retrieve a SEPA beneficiary endpoint instead. This endpoint
            remains available for international beneficiaries until a new endpoint supporting
            international beneficiary retrieval is released.

        Args:
            id (str): The ID of the beneficiary to retrieve.
                Example: "e72f4e63-9f27-4415-8781-adb46a859c7f"

        Returns:
            out(Dict): A dictionary containing the beneficiary details.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/beneficiaries/{id}")

    async def untrust_a_list_of_beneficiaries(self, ids: List[str]) -> Dict[str, Any]:
        """
        Untrusts up to 400 beneficiaries for the authenticated organization.

        Note: This endpoint will be deprecated on March 31, 2026. For SEPA beneficiaries,
        please use the Untrust SEPA beneficiaries endpoint instead. This endpoint
        remains available for international beneficiaries until a new endpoint supporting
        international beneficiary untrusting is released.

        Args:
            ids (List[str]): List of beneficiary IDs to untrust.
                Example: ["ce91bc4e-68d6-4ab0-bfab-4a9403f7f316"]

        Returns:
            out(Dict): A dictionary containing the untrusted beneficiaries.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        payload = {"ids": ids}
        return await self.api_client.patch("/beneficiaries/untrust", json=payload)

    async def list_sepa_beneficiaries(
        self,
        iban: Optional[List[str]] = None,
        status: Optional[List[str]] = None,
        trusted: Optional[bool] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 25,
        sort_by: Optional[str] = "updated_at:desc",
    ) -> Dict[str, Any]:
        """
        Return the list of SEPA beneficiaries for the authenticated organization.

        Args:
            iban (Optional[List[str]], optional): Filter by IBAN.
            status (Optional[List[str]], optional): Filter by status. Available options: pending, validated, declined.
            trusted (Optional[bool], optional): Filter by trusted status.
            page (Optional[int], optional): Page number. Default: 1.
            per_page (Optional[int], optional): Number of items per page. Default: 25.
            sort_by (Optional[str], optional): Sort by property and direction (e.g. "updated_at:desc"). Default: updated_at:desc.

        Returns:
            out(Dict): A dictionary containing the list of SEPA beneficiaries.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if iban:
            params["iban[]"] = iban
        if status:
            params["status[]"] = status
        if trusted is not None:
            params["trusted"] = trusted
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page
        if sort_by:
            params["sort_by"] = sort_by

        return await self.api_client.get("/sepa/beneficiaries", params)

    async def retrieve_a_sepa_beneficiary(self, id: str) -> Dict[str, Any]:
        """
        Returns a given SEPA beneficiary by ID.

        Args:
            id (str): Beneficiary ID.

        Returns:
            out(Dict): A dictionary containing the SEPA beneficiary.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/sepa/beneficiaries/{id}")

    async def upload_an_attachment(
        self, file_path: str, idempotency_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Uploads a single attachment (JPEG, PNG or PDF).

        This operation will enable you to link the uploaded attachment to an external transfer
        (through POST /v2/external_transfers or POST /v2/external_transfers/checkout).

        Args:
            file_path (str): Path to the file to upload (JPEG, PNG or PDF).
            idempotency_key (Optional[str], optional): Optional. This endpoint supports idempotency for safely retrying
                requests without accidentally performing the same operation twice.
                Example: "4668ac59-4e5c-4e51-9d01-fc5c33c79ddd"

        Returns:
            out(Dict): A dictionary containing information about the uploaded attachment.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                data = {}
                if idempotency_key:
                    data["idempotency_key"] = idempotency_key
                return await self.api_client.post(
                    "/attachments", data=data, files=files
                )
        except Exception as e:
            return {"errors": [{"detail": str(e)}]}

    async def retrieve_an_attachment(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the attachment identified by the id path parameter.

        In the Qonto app, attachments are files uploaded onto transactions by users.
        Attachments typically correspond to the invoice or receipt, and
        are used to justify the transactions from a bookkeeping standpoint.

        You can retrieve the IDs of those attachments inside each transaction object, by calling /v2/transactions.

        Probative attachment is another version of attachment, compliant with PADES standard.

        Note: For security reasons, the url you retrieve for each attachment is only valid for 30 minutes.
        If you need to download the file after more than 30 minutes, you will need to perform another
        authenticated call in order to generate a new valid URL.

        Args:
            id (str): The ID of the attachment to retrieve.
                Example: "e7274e43-9f27-4a15-8781-adb44a859c7f"

        Returns:
            out(Dict): A dictionary containing the attachment details.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/attachments/{id}")

    async def list_labels(
        self, page: Optional[str] = None, per_page: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves all the labels for the authenticated organization.

        Args:
            page (Optional[str], optional): Returned page of Pagination.
            per_page (Optional[str], optional): Number of labels per page (of Pagination).

        Returns:
            out(Dict): A dictionary containing the list of labels for the authenticated organization.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page

        return await self.api_client.get("/labels", params)

    async def retrieve_a_label(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the label identified by the id path parameter.

        Args:
            id (str): Uniquely identifies the label.
                Example: "2d96a3fd-1748-4ed4-a590-48066ae9e1cb"

        Returns:
            out(Dict): A dictionary containing the label details.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/labels/{id}")

    async def list_memberships(
        self, page: Optional[str] = None, per_page: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves all the memberships for the authenticated organization.

        A member is a user who's been granted access to the Qonto account of a company.
        There is currently no limit to the number of memberships a company can have.

        Args:
            page (Optional[str], optional): Returned page.
            per_page (Optional[str], optional): Number of memberships per page (of Pagination).

        Returns:
            out(Dict): A dictionary containing the list of memberships for the authenticated organization.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page

        return await self.api_client.get("/memberships", params)

    async def retrieve_the_authenticated_organization_and_list_bank_accounts(
        self, include_external_accounts: Optional[bool] = False
    ) -> Dict[str, Any]:
        """
        Retrieves the details and the list of bank accounts for the authenticated organization.

        The bank account's id or iban will be required to retrieve the list
        of transactions inside that bank account, using GET /v2/transactions.

        Args:
            include_external_accounts (Optional[bool], optional): By default includes only Qonto accounts.
                Set to 'true' if you also want to include your connected externals account(s).
                Default: False.

        Returns:
            out(Dict): A dictionary containing the organization details and its bank accounts.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if include_external_accounts:
            params["include_external_accounts"] = "true"

        return await self.api_client.get("/organization", params)

    async def upload_an_attachment_to_a_transaction(
        self, id: str, file_path: str, idempotency_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Uploads a single attachment (JPEG, PNG or PDF) to the transaction identified by the id path parameter.

        Note: The uploaded file will be processed in the background. This means that the
        created attachment will not be visible immediately.

        Args:
            id (str): Identifies the transaction to which the attachment will be uploaded.
                Example: "2731e51c-c37f-437f-b018-45efeac89a30"
            file_path (str): Path to the file to upload (JPEG, PNG or PDF).
            idempotency_key (Optional[str], optional): Optional. This API supports idempotency for safely retrying
                requests without accidentally performing the same operation twice.
                Example: "4668ac59-4e5c-4e51-9d01-fc5c33c79ddd"

        Returns:
            out(Dict): An empty dictionary.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                data = {}
                if idempotency_key:
                    data["idempotency_key"] = idempotency_key
                return await self.api_client.post(
                    f"/transactions/{id}/attachments", data=data, files=files
                )
        except Exception as e:
            return {"errors": [{"detail": str(e)}]}

    async def list_attachments_for_a_transaction(
        self, id: str, page: Optional[str] = None, per_page: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves all the attachments for the transaction identified by the id path parameter.

        In the Qonto app, attachments are files uploaded onto transactions by users.
        Attachments typically correspond to the invoice or receipt, and are used to justify the transactions
        from a bookkeeping standpoint.
        Note: For security reasons, the url you retrieve for each attachment is only valid for 30 minutes.
        If you need to download the file after more than 30 minutes, you will need to perform another
        authenticated call in order to generate a new download URL.

        Args:
            id (str): Identifies the transaction to retrieve attachments for.
                Example: "aaa8e6fa-0b4c-4749-9a97-bda8efa9e323"
            page (Optional[str], optional): Returned page of Pagination.
            per_page (Optional[str], optional): Number of attachments per page (of Pagination).

        Returns:
            out(Dict): A dictionary containing the list of attachments for the transaction.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page

        return await self.api_client.get(f"/transactions/{id}/attachments", params)

    async def remove_an_attachment_from_a_transaction(
        self, transaction_id: str, attachment_id: str
    ) -> Dict[str, Any]:
        """
        Removes a single attachment from the transaction identified by the id path parameter.

        In the Qonto app, attachments are files uploaded onto transactions by users.
        Attachments typically correspond to the invoice or receipt, and are used to
        justify the transactions from a bookkeeping standpoint.

        Args:
            transaction_id (str): The ID of the transaction. Example: "644cf847-125e-4ec9-92bb-8d99aee6dbc"
            attachment_id (str): The ID of the attachment to remove.

        Returns:
            out(Dict): Returns {"status": "success", "status_code": ...} on success.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.delete(
            f"/transactions/{transaction_id}/attachments/{attachment_id}"
        )

    async def remove_all_attachments_from_a_transaction(
        self, id: str
    ) -> Dict[str, Any]:
        """
        Removes all attachments from the transaction identified by the id path parameter.

        Args:
            id (str): Identifies the transaction from which all attachments will be removed.
                Example: "275bad5e-6cb4-409e-88a8-ab4336a3bd57"

        Returns:
            out(Dict): An empty dictionary.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.delete(f"/transactions/{id}/attachments")

    async def list_transactions(
        self,
        bank_account_id: Optional[str] = None,
        iban: Optional[str] = None,
        includes: Optional[List[str]] = None,
        status: Optional[List[str]] = None,
        updated_at_from: Optional[str] = None,
        updated_at_to: Optional[str] = None,
        settled_at_from: Optional[str] = None,
        settled_at_to: Optional[str] = None,
        side: Optional[List[str]] = None,
        operation_type: Optional[List[str]] = None,
        with_attachments: Optional[bool] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the list of transactions for the bank account identified by the
        bank_account_id or iban query parameter.

        You can filter (only retrieve the latest transactions) and sort this list by using query parameters.

        Args:
            bank_account_id (Optional[str], optional): ID of the bank account for which transactions will be retrieved.
            iban (Optional[str], optional): IBAN of the bank account for which transactions will be retrieved.
            includes (Optional[List[str]], optional): Additional resources to include in the response. Possible: "labels", "attachments"
            status (Optional[List[str]], optional): Filter transactions by their status. Possible: "pending", "declined", "completed"
            updated_at_from (Optional[str], optional): Filter by updated_at property (ISO8601).
            updated_at_to (Optional[str], optional): Filter by updated_at property (ISO8601).
            settled_at_from (Optional[str], optional): Filter by settled_at property (ISO8601).
            settled_at_to (Optional[str], optional): Filter by settled_at property (ISO8601).
            side (Optional[List[str]], optional): Filter by transaction side. Possible: "debit", "credit"
            operation_type (Optional[List[str]], optional): Filter by operation type.
            with_attachments (Optional[bool], optional): Filter on the presence of attachments.
            sort_by (Optional[str], optional): Sorting. Format: "PROPERTY:ORDER"
            page (Optional[int], optional): Pagination page number.
            per_page (Optional[int], optional): Number of transactions per page.

        Returns:
            out(Dict): List of transactions for the specified bank account.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if bank_account_id:
            params["bank_account_id"] = bank_account_id
        if iban:
            params["iban"] = iban
        if includes:
            params["includes[]"] = includes
        if status:
            params["status[]"] = status
        if updated_at_from:
            params["updated_at_from"] = updated_at_from
        if updated_at_to:
            params["updated_at_to"] = updated_at_to
        if settled_at_from:
            params["settled_at_from"] = settled_at_from
        if settled_at_to:
            params["settled_at_to"] = settled_at_to
        if side:
            params["side[]"] = side
        if operation_type:
            params["operation_type[]"] = operation_type
        if with_attachments is not None:
            params["with_attachments"] = with_attachments
        if sort_by:
            params["sort_by"] = sort_by
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page

        return await self.api_client.get("/transactions", params)

    async def retrieve_a_transaction(
        self, transaction_id: str, includes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Retrieves the transaction identified by the id path parameter.

        Args:
            transaction_id (str): UUID of the transaction to retrieve.
                Example: "7b7a5de6-1983-47d2-89fd-bef44dd7bef5"
            includes (Optional[List[str]], optional): Use this parameter to embed the associated resources
                (labels, attachments and/or VAT details) of the transaction in the JSON response.
                Available options: "vat_details", "labels", "attachments"

        Returns:
            out(Dict): The transaction object with its details.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if includes:
            params["includes[]"] = includes

        return await self.api_client.get(f"/transactions/{transaction_id}", params)

    async def create_an_internal_transfer(
        self,
        debit_iban: str,
        credit_iban: str,
        reference: str,
        amount: str,
        currency: str = "EUR",
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Creates a single instant transfer between 2 bank accounts of the authenticated organization.

        You can obtain the bank accounts' IBAN through the GET /organization endpoint.

        Args:
            debit_iban (str): IBAN of account to debit.
            credit_iban (str): IBAN of account to credit.
            reference (str): Details to further describe the transfer (max 90 chars).
            amount (str): Amount of the transaction as a valid decimal monetary value.
            currency (str, optional): Only accepts "EUR". Default is "EUR".
            idempotency_key (Optional[str], optional): For safely retrying requests
                without accidentally performing the same operation twice.

        Returns:
            out(Dict): The created internal transfer object.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        payload = {
            "internal_transfer": {
                "debit_iban": debit_iban,
                "credit_iban": credit_iban,
                "reference": reference,
                "amount": amount,
                "currency": currency,
            }
        }

        data = {}
        if idempotency_key:
            data["idempotency_key"] = idempotency_key

        return await self.api_client.post(
            "/internal_transfers", data=data, json=payload
        )

    async def list_requests(
        self,
        status: Optional[List[str]] = None,
        request_type: Optional[List[str]] = None,
        created_at_from: Optional[str] = None,
        processed_at_from: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the list of requests for the authenticated organization.

        You can filter, sort, retrieve a specific request type and sort this list by using query parameters.

        Args:
            status (Optional[List[str]], optional): Filter requests by their status. Options: pending, approved, declined, expired, canceled.
            request_type (Optional[List[str]], optional): Filter requests by request type. Options: flash_card, credit_transfer, sepa_transfer, direct_debit, payroll_invoice.
            created_at_from (Optional[str], optional): Filter by created_at (ISO-8601). Example: "2023-01-10T17:37:51.000Z"
            processed_at_from (Optional[str], optional): Filter by processed_at (ISO-8601). Example: "2023-01-10T17:37:51.000Z"
            sort_by (Optional[str], optional): Sort by property and direction (e.g., "processed_at:desc", "created_at:asc").
            page (Optional[int], optional): Pagination page.
            per_page (Optional[int], optional): Number of requests per page.

        Returns:
            out(Dict): Returns the list of requests.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if status:
            params["status[]"] = status
        if request_type:
            params["request_type[]"] = request_type
        if created_at_from:
            params["created_at_from"] = created_at_from
        if processed_at_from:
            params["processed_at_from"] = processed_at_from
        if sort_by:
            params["sort_by"] = sort_by
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page

        return await self.api_client.get("/requests", params)

    async def create_supplier_invoices(
        self,
        supplier_invoices: List[Dict[str, Any]],
        meta: Optional[Union[Dict[str, Any], str]] = None,
    ) -> Dict[str, Any]:
        """
        Creates supplier invoices in bulk for the authenticated organization by uploading files.

        Args:
            supplier_invoices (List[Dict]): List of supplier invoice objects. Each object should contain:
                Required fields:
                - file (str): Path to the file to upload (JPEG, PNG or PDF).
                - idempotency_key (str): Unique string that identifies an invoice. Used by Qonto to prevent performing the same operation twice.
            meta (Optional[Union[Dict, str]], optional): Additional metadata for the request.
                Note: If provided, must contain at least one of 'integration_type' and 'connector' keys.
                Example: {"integration_type": "amazon", "connector": "grover"}
                Or: {"integration_type": "amazon"}
                Or: {"connector": "grover"}

        Returns:
            out(Dict): A dictionary containing the created supplier invoices.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        data = {}
        if meta:
            data["meta"] = meta if isinstance(meta, str) else json.dumps(meta)

        files = []
        for i, invoice in enumerate(supplier_invoices):
            if "file" not in invoice or "idempotency_key" not in invoice:
                return {
                    "error": f"Invoice {i} missing required 'file' or 'idempotency_key' field"
                }
            file_path = invoice["file"]
            idempotency_key = invoice["idempotency_key"]
            try:
                file_obj = open(file_path, "rb")
                files.append(
                    (
                        f"supplier_invoices[][file]",
                        (Path(file_path).name, file_obj, "application/pdf"),
                    )
                )
                files.append(
                    ("supplier_invoices[][idempotency_key]", (None, idempotency_key))
                )
            except Exception as e:
                return {"error": f"Error opening file {file_path}: {str(e)}"}

        try:
            return await self.api_client.post(
                "/supplier_invoices/bulk", data=data, files=files
            )
        finally:
            for _, file_obj in files:
                if hasattr(file_obj, "close"):
                    file_obj.close()

    async def list_supplier_invoices(
        self,
        filter_status: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = 1,
        sort_by: Optional[str] = None,
        filter_created_at_from: Optional[str] = None,
        filter_created_at_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the list of supplier invoices for the authenticated organization.

        You can filter (e.g. only retrieve the latest supplier invoices) and sort this list by using query parameters.

        Args:
            filter_status (Optional[str], optional): Filter invoices by their status.
            page (Optional[int], optional): Paginated page id.
            per_page (Optional[int], optional): Number of invoices per page (range: 1-100). Default is 1.
            sort_by (Optional[str], optional): Sort invoices by a specific property and order.
                Format: {property}_{asc|desc}. (e.g., created_at_desc)
                Properties: created_at, file_name, supplier_name, payment_date, due_date, scheduled_date, total_amount.
            filter_created_at_from (Optional[str], optional): Filter invoices by their created_at property (ISO 8601).
            filter_created_at_to (Optional[str], optional): Filter invoices by their created_at property (ISO 8601).

        Returns:
            out(Dict): A dictionary containing the list of supplier invoices.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if filter_status:
            params["filter[status]"] = filter_status
        if page is not None:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page
        if sort_by:
            params["sort_by"] = sort_by
        if filter_created_at_from:
            params["filter[created_at_from]"] = filter_created_at_from
        if filter_created_at_to:
            params["filter[created_at_to]"] = filter_created_at_to

        return await self.api_client.get("/supplier_invoices", params)

    async def retrieve_a_supplier_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Retrieves the supplier invoice identified by the id path parameter.

        Args:
            invoice_id (str): The ID of the supplier invoice.
                Example: "a9d359b2-aed0-4dce-c87a-cdf4aa5ba54"

        Returns:
            out(Dict): The supplier invoice object with all its details.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/supplier_invoices/{invoice_id}")

    async def create_a_client_invoice(
        self,
        client_id: str,
        issue_date: str,
        due_date: str,
        number: str,
        payment_methods: Dict[str, Any],
        items: List[Dict[str, Any]],
        currency: str = "EUR",
        performance_date: Optional[str] = None,
        status: Optional[str] = None,
        purchase_order: Optional[str] = None,
        terms_and_conditions: Optional[str] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        report_einvoicing: Optional[bool] = None,
        payment_reporting: Optional[Dict[str, Any]] = None,
        welfare_fund: Optional[Dict[str, Any]] = None,
        withholding_tax: Optional[Dict[str, Any]] = None,
        stamp_duty_amount: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Creates a single client invoice for the authenticated organization.

        Args:
            client_id (str): The ID of the client for whom the invoice is created.
            issue_date (str): The date the initiator has issued or shared the invoice as legally viable. Format: YYYY-MM-DD.
            due_date (str): The invoice's payment deadline. Format: YYYY-MM-DD.
            number (str): The invoice's number. Maximum length: 40.
            currency (str, optional): The invoice's currency. Currently, only "EUR" is allowed. Default: "EUR".
            payment_methods (Dict): Contains payment method details for the invoice.
                Required fields:
                - iban (str): The beneficiary's International Bank Account Number (IBAN). Must follow ISO 13616 format,
                start with two letters, followed by 26 digits. Must be associated to a Qonto account.
            items (List[Dict]): List of invoice items. Each item should contain:
                Required fields:
                - title (str): The item's title. Maximum length: 48.
                - quantity (str): Quantity of the specific product or service being sold. Decimals separated by period.
                - unit_price (Dict): Contains value (str, required) and currency (str, required).
                - vat_rate (str): VAT rate applicable for that particular item. Written in decimals.
                Optional fields:
                - description (str): Description of the product or service being sold. Maximum length: 384.
                - unit (str): The item's unit. See documentation for available units (meter, liter, etc.).
                - vat_exemption_reason (str): VAT exemption reason when vat_rate is equal to 0. Available options: N1-N7.
                - discount (Dict): Contains type ("percentage" or "absolute") and value (str).
            performance_date (Optional[str], optional): The date the service was performed. Format: YYYY-MM-DD.
            status (Optional[str], optional): The status of the invoice. Available options: "draft", "unpaid". Default: "unpaid".
            purchase_order (Optional[str], optional): Purchase order data. Maximum length: 40.
            terms_and_conditions (Optional[str], optional): Additional notes. Maximum length: 525.
            header (Optional[str], optional): Invoice header text.
            footer (Optional[str], optional): Invoice footer text.
            settings (Optional[Dict], optional): Collection of properties to override organization settings for this invoice.
                Optional fields:
                - vat_number (str): Example: "FR12345678"
                - company_leadership (str): Example: "Jan Mueller"
                - district_court (str): Example: "Munich"
                - commercial_register_number (str): Example: "HRB12345B"
                - tax_number (str): Example: "123/123/1234"
                - legal_capital_share (Dict): Contains value (str) and currency (str)
                - transaction_type (str): Available options: "goods", "services", "goods_and_services"
                - vat_payment_condition (str): Available options: "on_receipts", "compensated_for_sales"
                - discount_conditions (str): Example: "Pas d'escompte accordé pour paiement anticipé."
                - late_payment_penalties (str): Example: "En cas de non-paiement à la date d'échéance, des pénalités..."
                - legal_fixed_compensation (str): Example: "Tout retard de paiement entraînera une indemnité forfaitaire..."
            report_einvoicing (Optional[bool], optional): For Italian organizations only. Controls e-invoicing to SdI.
            payment_reporting (Optional[Dict], optional): For Italian organizations only. Payment methods and conditions.
                Required fields:
                - conditions (str): Payment conditions. Available options: "TP01", "TP02", "TP03"
                - method (str): Payment method. Available options: "MP01" through "MP22"
            welfare_fund (Optional[Dict], optional): For Italian organizations only. Pension contributions object.
                Required fields:
                - type (str): Welfare fund type. Available options: "TC01" through "TC22"
                - rate (str): Welfare fund rate (4-6 chars). Example: "0.0001"
            withholding_tax (Optional[Dict], optional): For Italian organizations and Spanish freelancers only.
                Required fields:
                - reason (str): Withholding tax reason. Available options: "RF01" through "RF06"
                - rate (str): Withholding tax rate (4-6 chars). Example: "0.01"
                - payment_reason (str): Payment reason (1-2 chars). Example: "L1"
            stamp_duty_amount (Optional[str], optional): For Italian organizations only. Amount applicable on VAT-excluded invoices. Length: 4-15.
            idempotency_key (Optional[str], optional): For safely retrying requests without performing the same operation twice.

        Returns:
            out(Dict): A dictionary containing the created client invoice.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        payload = {
            "client_id": client_id,
            "issue_date": issue_date,
            "due_date": due_date,
            "number": number,
            "currency": currency,
            "payment_methods": payment_methods,
            "items": items,
        }

        if performance_date:
            payload["performance_date"] = performance_date
        if status:
            payload["status"] = status
        if purchase_order:
            payload["purchase_order"] = purchase_order
        if terms_and_conditions:
            payload["terms_and_conditions"] = terms_and_conditions
        if header:
            payload["header"] = header
        if footer:
            payload["footer"] = footer
        if settings:
            payload["settings"] = settings
        if report_einvoicing is not None:
            payload["report_einvoicing"] = report_einvoicing
        if payment_reporting:
            payload["payment_reporting"] = payment_reporting
        if welfare_fund:
            payload["welfare_fund"] = welfare_fund
        if withholding_tax:
            payload["withholding_tax"] = withholding_tax
        if stamp_duty_amount:
            payload["stamp_duty_amount"] = stamp_duty_amount

        data = {}
        if idempotency_key:
            data["idempotency_key"] = idempotency_key

        return await self.api_client.post("/client_invoices", data=data, json=payload)

    async def list_client_invoices(
        self,
        filter_status: Optional[str] = None,
        filter_created_at_from: Optional[str] = None,
        filter_created_at_to: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = 1,
        sort_by: Optional[str] = "created_at:desc",
    ) -> Dict[str, Any]:
        """
        Retrieves the list of client invoices for the authenticated organization.

        You can filter (e.g. only retrieve the latest client invoices) and sort this list by using query parameters.

        Args:
            filter_status (Optional[str], optional): Filter invoices by their status.
                Available options: draft, unpaid, paid, canceled.
            filter_created_at_from (Optional[str], optional): Filter invoices by their created_at property from this date (ISO 8601).
            filter_created_at_to (Optional[str], optional): Filter invoices by their created_at property up to this date (ISO 8601).
            page (Optional[int], optional): Returned page id. For pagination.
            per_page (Optional[int], optional): Number of invoices per page. Range: 1-100. Default = 1.
            sort_by (Optional[str], optional): Sort invoices by their created_at property: "created_at:desc" or "created_at:asc". Default = "created_at:desc".

        Returns:
            out(Dict): A dictionary containing the list of client invoices.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_created_at_from:
            params["filter[created_at_from]"] = filter_created_at_from
        if filter_created_at_to:
            params["filter[created_at_to]"] = filter_created_at_to
        if page is not None:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page
        if sort_by:
            params["sort_by"] = sort_by

        return await self.api_client.get("/client_invoices", params)

    async def retrieve_a_client_invoice(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the client invoice identified by the id path parameter.

        Args:
            id (str): UUID of the client invoice to retrieve.

        Returns:
            out(Dict): The client invoice identified by the id path parameter.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/client_invoices/{id}")

    async def list_credit_notes(
        self,
        filter_created_at_from: Optional[str] = None,
        filter_created_at_to: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = 1,
        sort_by: Optional[str] = "created_at:desc",
    ) -> Dict[str, Any]:
        """
        Retrieves the list of credit notes for the authenticated organization.

        You can filter (ex: only retrieve the latest credit notes) and sort this list by using query parameters.

        Args:
            filter_created_at_from (Optional[str], optional): Filter by their created_at property (ISO 8601).
            filter_created_at_to (Optional[str], optional): Filter by their created_at property (ISO 8601).
            page (Optional[int], optional): Returned page id. For pagination.
            per_page (Optional[int], optional): Number of credit notes per page. Required range: 1-100. Default = 1.
            sort_by (Optional[str], optional): Sort by created_at in "asc" or "desc" order. Default is created_at:desc.

        Returns:
            out(Dict): Returns the list of credit notes.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if filter_created_at_from:
            params["filter[created_at_from]"] = filter_created_at_from
        if filter_created_at_to:
            params["filter[created_at_to]"] = filter_created_at_to
        if page is not None:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page
        if sort_by:
            params["sort_by"] = sort_by

        return await self.api_client.get("/credit_notes", params)

    async def retrieve_a_credit_note(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the credit note identified by the id path parameter.

        Args:
            id (str): ID of the credit note

        Returns:
            out(Dict): Returns the credit note identified by the id path parameter.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/credit_notes/{id}")

    async def create_a_client(
        self,
        name: str,
        type: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        vat_number: Optional[str] = None,
        tax_identification_number: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        zip_code: Optional[str] = None,
        province_code: Optional[str] = None,
        country_code: Optional[str] = None,
        billing_address: Optional[Dict[str, Any]] = None,
        delivery_address: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Creates a single client for the authenticated organization.

        Args:
            name (str): Name of the client. Required if type is company.
            type (str): Client type. 'individual', 'company', or 'freelancer'.
            email (str): E-mail address of the client.
            first_name (str, optional): First name. Required if type is individual or freelancer.
            last_name (str, optional): Last name. Required if type is individual or freelancer.
            vat_number (str, optional): Client's VAT number.
            tax_identification_number (str, optional): Client's Tax ID.
            address (str, optional): Address of the client.
            city (str, optional): City.
            zip_code (str, optional): Zip code. For Italy, must be 5 chars.
            province_code (str, optional): Province code. Required for Italian orgs.
            country_code (str, optional): ISO 3166-1 alpha-2 country code.
            billing_address (dict, optional): Billing address.
            delivery_address (dict, optional): Delivery address.

        Returns:
            out(Dict): A dictionary containing the created client.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        payload = {"name": name, "type": type, "email": email}
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if vat_number:
            payload["vat_number"] = vat_number
        if tax_identification_number:
            payload["tax_identification_number"] = tax_identification_number
        if address:
            payload["address"] = address
        if city:
            payload["city"] = city
        if zip_code:
            payload["zip_code"] = zip_code
        if province_code:
            payload["province_code"] = province_code
        if country_code:
            payload["country_code"] = country_code
        if billing_address:
            payload["billing_address"] = billing_address
        if delivery_address:
            payload["delivery_address"] = delivery_address

        return await self.api_client.post("/clients", json=payload)

    async def list_clients(
        self,
        filter_obj: Optional[Dict[str, Any]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = 25,
        sort_by: Optional[str] = "name:asc",
    ) -> Dict[str, Any]:
        """
        Retrieves the list of clients for the authenticated organization.

        You can filter (ex: only retrieve the latest clients) and sort this list by using query parameters.

        Args:
            filter_obj (Optional[dict], optional): Clients can be filtered based on their tax_identification_number,
                vat_number, or email. The value must at least contain 2 characters minimum.
            page (Optional[int], optional): Returned page id. For pagination.
            per_page (Optional[int], optional): Number of clients per page. Default: 25.
            sort_by (Optional[str], optional): Sort by 'created_at' or 'name', 'asc' or 'desc'. Default: name:asc.

        Returns:
            out(Dict): Returns the list of clients.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if filter_obj:
            params["filter[]"] = filter_obj
        if page is not None:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page
        if sort_by:
            params["sort_by"] = sort_by

        return await self.api_client.get("/clients", params)

    async def retrieve_a_client(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the client identified by the id path parameter.

        Args:
            id (str): ID of the client

        Returns:
            out(Dict): Returns the client identified by the id path parameter.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/clients/{id}")

    async def list_statements(
        self,
        bank_account_ids: Optional[List[str]] = None,
        ibans: Optional[List[str]] = None,
        period_from: Optional[str] = None,
        period_to: Optional[str] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 100,
        sort_by: Optional[str] = "period:desc",
    ) -> Dict[str, Any]:
        """
        Retrieves the list of statements for the authenticated organization.

        Args:
            bank_account_ids (Optional[List[str]], optional): Filter statements by their bank_account_id.
                Note: bank_account_ids and ibans are mutually exclusive.
            ibans (Optional[List[str]], optional): Filter statements by their iban.
                Note: ibans and bank_account_ids are mutually exclusive.
            period_from (Optional[str], optional): Filter for statements from this period (ISO 8601). Example: "01-2023"
            period_to (Optional[str], optional): Filter for statements up to this period (ISO 8601). Example: "12-2023"
            page (Optional[int], optional): Returned page. Defaults to 1.
            per_page (Optional[int], optional): Number of statements per page. Defaults to 100. Range: 1-100.
            sort_by (Optional[str], optional): Sort by statement period, asc or desc. Defaults to "period:desc".

        Returns:
            out(Dict): Returns the list of statements.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if bank_account_ids:
            params["bank_account_ids[]"] = bank_account_ids
        if ibans:
            params["iban[]"] = ibans
        if period_from:
            params["period_from"] = period_from
        if period_to:
            params["period_to"] = period_to
        if page != 1:
            params["page"] = page
        if per_page != 100:
            params["per_page"] = per_page
        if sort_by != "period:desc":
            params["sort_by"] = sort_by

        return await self.api_client.get("/statements", params)

    async def retrieve_a_statement(self, id: str) -> Dict[str, Any]:
        """
        Retrieves the statement identified by the id path parameter.

        Args:
            id (str): Unique identifier of the statement.
                Example: "0854c799-6365-4e85-8487-e835290bcee8"

        Returns:
            out(Dict): The statement data.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/statements/{id}")

    async def list_business_accounts(
        self, page: Optional[int] = 1, per_page: Optional[int] = 100
    ) -> Dict[str, Any]:
        """
        Retrieves a list of all business accounts.

        You can use this endpoint when you need to display account details of all business accounts.

        Note on field visibility:
        - Fields available to all users: id, name, status, main, organization_id
        - Fields available to users with Balance Authorization Read: currency, balance, balance_cents, authorized_balance, authorized_balance_cents
        - Owners and admins can access all fields

        Args:
            page (Optional[int], optional): Page number for pagination. Must be greater than 0. Defaults to 1.
            per_page (Optional[int], optional): Number of business accounts per page. Must be between 1 and 100. Defaults to 100.

        Returns:
            out(Dict): List of business accounts retrieved successfully.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        params = {}
        if page != 1:
            params["page"] = page
        if per_page != 100:
            params["per_page"] = per_page

        return await self.api_client.get("/bank_accounts", params)

    async def get_a_business_account(self, id: str) -> Dict[str, Any]:
        """
        Retrieves detailed information about a specific business account identified by its ID.

        It is useful for retrieving up-to-date information, including the current
        balance and authorized balance of the account.

        You can use this endpoint when you need to display account details
        or verify available funds before initiating a transfer.

        Note on field visibility:
        - Fields available to all users: id, name, status, main, organization_id
        - Fields available to users with Balance Authorization Read: currency,
        balance, balance_cents, authorized_balance, authorized_balance_cents
        - Owners and admins can access all fields

        Args:
            id (str): ID of the business account to retrieve

        Returns:
            out(Dict): Business account retrieved successfully.
            If there's an error, returns a dictionary with an 'errors' key.
        """
        return await self.api_client.get(f"/bank_accounts/{id}")
