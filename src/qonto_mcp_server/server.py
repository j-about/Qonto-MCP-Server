import logging
from typing import (
    Dict,
    List,
    Optional
)

import httpx
from mcp.server.fastmcp import FastMCP

from qonto_mcp_server.config import (
    API_KEY,
    BASE_URL,
    STAGING_TOKEN
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

mcp = FastMCP("Qonto MCP Server")

@mcp.tool()
async def list_external_transfers(
    status: Optional[List[str]] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    scheduled_date_from: Optional[str] = None,
    scheduled_date_to: Optional[str] = None,
    beneficiary_ids: Optional[List[str]] = None,
    sort_by: Optional[str] = None,
    page: Optional[str] = None,
    per_page: Optional[str] = None,
) -> Dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/external_transfers"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def retrieve_an_external_transfer(id: str) -> Dict:
    """
    Retrieves the external transfer identified by the given ID.

    Args:
        id (str): The ID of the external transfer to retrieve.
            Example: "7b7a5ed6-3983-47b2-89fd-0cf44bd7bef9"

    Returns:
        out(Dict): A dictionary containing the external transfer details.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/external_transfers/{id}"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def list_beneficiaries(
    trusted: Optional[bool] = None,
    status: Optional[List[str]] = None,
    iban: Optional[List[str]] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    sort_by: Optional[str] = "updated_at:desc",
    page: Optional[str] = None,
    per_page: Optional[str] = None,
) -> Dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/beneficiaries"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN
    
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
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def retrieve_a_beneficiary(id: str) -> Dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/beneficiaries/{id}"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def list_sepa_beneficiaries(
    iban: Optional[List[str]] = None,
    status: Optional[List[str]] = None,
    trusted: Optional[bool] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 25,
    sort_by: Optional[str] = "updated_at:desc",
) -> Dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/sepa/beneficiaries"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def retrieve_a_sepa_beneficiary(id: str) -> Dict:
    """
    Returns a given SEPA beneficiary by ID.

    Args:
        id (str): Beneficiary ID.

    Returns:
        out(Dict): A dictionary containing the SEPA beneficiary.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/sepa/beneficiaries/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def retrieve_an_attachment(id: str) -> Dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/attachments/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def list_labels(
    page: Optional[str] = None,
    per_page: Optional[str] = None
) -> Dict:
    """
    Retrieves all the labels for the authenticated organization.

    Args:
        page (Optional[str], optional): Returned page of Pagination.
        per_page (Optional[str], optional): Number of labels per page (of Pagination).

    Returns:
        out(Dict): A dictionary containing the list of labels for the authenticated organization.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/labels"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    params = {}
    if page:
        params["page"] = page
    if per_page:
        params["per_page"] = per_page

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def retrieve_a_label(id: str) -> Dict:
    """
    Retrieves the label identified by the id path parameter.

    Args:
        id (str): Uniquely identifies the label.
            Example: "2d96a3fd-1748-4ed4-a590-48066ae9e1cb"

    Returns:
        out(Dict): A dictionary containing the label details.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/labels/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def list_memberships(
    page: Optional[str] = None,
    per_page: Optional[str] = None
) -> Dict:
    """
    Retrieves all the memberships for the authenticated organization.

    A member is a user who's been granted access to the Qonto account of a company.
    There is currently no limit to the number of memberships a company can have.

    Args:
        page (Optional[str], optional): Returned page.
        per_page (Optional[str], optional): Number of memberships per page (of Pagination).

    Returns:
        out(Dict): A dictionary containing the list of memberships for the authenticated organization.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/memberships"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    params = {}
    if page:
        params["page"] = page
    if per_page:
        params["per_page"] = per_page

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def retrieve_the_authenticated_organization_and_list_bank_accounts(
    include_external_accounts: Optional[bool] = False
) -> Dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/organization"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN
    
    params = {}
    if include_external_accounts:
        params["include_external_accounts"] = "true"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def list_attachments_for_a_transaction(
    id: str, 
    page: Optional[str] = None,
    per_page: Optional[str] = None
) -> Dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/transactions/{id}/attachments"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN
    
    params = {}
    if page:
        params["page"] = page
    if per_page:
        params["per_page"] = per_page
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def list_transactions(
    bank_account_id: Optional[str] = None,
    iban: Optional[str] = None,
    includes: Optional[list[str]] = None,
    status: Optional[list[str]] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    settled_at_from: Optional[str] = None,
    settled_at_to: Optional[str] = None,
    side: Optional[list[str]] = None,
    operation_type: Optional[list[str]] = None,
    with_attachments: Optional[bool] = None,
    sort_by: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/transactions"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN
    
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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def retrieve_a_transaction(
    transaction_id: str,
    includes: Optional[list[str]] = None
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/transactions/{transaction_id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    params = {}
    if includes:
        params["includes[]"] = includes

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def list_requests(
    status: Optional[list[str]] = None,
    request_type: Optional[list[str]] = None,
    created_at_from: Optional[str] = None,
    processed_at_from: Optional[str] = None,
    sort_by: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/requests"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def list_supplier_invoices(
    filter_status: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = 1,
    sort_by: Optional[str] = None,
    filter_created_at_from: Optional[str] = None,
    filter_created_at_to: Optional[str] = None
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/supplier_invoices"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def retrieve_a_supplier_invoice(invoice_id: str) -> dict:
    """
    Retrieves the supplier invoice identified by the id path parameter.

    Args:
        invoice_id (str): The ID of the supplier invoice.
            Example: "a9d359b2-aed0-4dce-c87a-cdf4aa5ba54"

    Returns:
        out(Dict): The supplier invoice object with all its details.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/supplier_invoices/{invoice_id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def list_client_invoices(
    filter_status: Optional[str] = None,
    filter_created_at_from: Optional[str] = None,
    filter_created_at_to: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = 1,
    sort_by: Optional[str] = "created_at:desc"
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/client_invoices"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def retrieve_a_client_invoice(id: str) -> dict:
    """
    Retrieves the client invoice identified by the id path parameter.

    Args:
        id (str): UUID of the client invoice to retrieve.

    Returns:
        out(Dict): The client invoice identified by the id path parameter.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/client_invoices/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

@mcp.tool()
async def list_credit_notes(
    filter_created_at_from: Optional[str] = None,
    filter_created_at_to: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = 1,
    sort_by: Optional[str] = "created_at:desc"
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/credit_notes"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def retrieve_a_credit_note(id: str) -> dict:
    """
    Retrieves the credit note identified by the id path parameter.

    Args:
        id (str): ID of the credit note

    Returns:
        out(Dict): Returns the credit note identified by the id path parameter.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/credit_notes/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def list_clients(
    filter_obj: Optional[dict] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = 25,
    sort_by: Optional[str] = "name:asc"
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/clients"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    params = {}
    if filter_obj:
        params["filter[]"] = filter_obj
    if page is not None:
        params["page"] = page
    if per_page:
        params["per_page"] = per_page
    if sort_by:
        params["sort_by"] = sort_by

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def retrieve_a_client(id: str) -> dict:
    """
    Retrieves the client identified by the id path parameter.

    Args:
        id (str): ID of the client

    Returns:
        out(Dict): Returns the client identified by the id path parameter.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/clients/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def list_statements(
    bank_account_ids: Optional[list[str]] = None,
    ibans: Optional[list[str]] = None,
    period_from: Optional[str] = None,
    period_to: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 100,
    sort_by: Optional[str] = "period:desc"
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/statements"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def retrieve_a_statement(id: str) -> dict:
    """
    Retrieves the statement identified by the id path parameter.

    Args:
        id (str): Unique identifier of the statement.
            Example: "0854c799-6365-4e85-8487-e835290bcee8"

    Returns:
        out(Dict): The statement data.
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/statements/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def list_business_accounts(
    page: Optional[int] = 1,
    per_page: Optional[int] = 100
) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/bank_accounts"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    params = {}
    if page != 1:
        params["page"] = page
    if per_page != 100:
        params["per_page"] = per_page

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}

        return response.json()

@mcp.tool()
async def get_a_business_account(id: str) -> dict:
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
        If there's an error, returns a dictionary with an 'error' key.
    """
    url = f"{BASE_URL}/bank_accounts/{id}"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.exception("%s", e)
            return {"error": str(e)}
        
        return response.json()

def serve():
    mcp.run()