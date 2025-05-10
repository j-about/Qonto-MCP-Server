from typing import (
    Dict,
    List,
    Optional
)

import httpx
from mcp.server.fastmcp import FastMCP

from config import (
    API_KEY,
    BASE_URL
)

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
        status: External transfers can be filtered by their status. This filter accepts an array of
               statuses. Available options: pending, processing, canceled, declined, settled.
        updated_at_from: Filter by updated_at property. This filter can be used in
                       combination with the updated_at_to query parameter to get external transfers
                       updated within a specific timeframe. Please use a valid date time format: ISO 8601.
        updated_at_to: Filter by updated_at property. This filter can be used in
                     combination with the updated_at_from query parameter to get external transfers
                     updated within a specific timeframe. Please use a valid date time format: ISO 8601.
        scheduled_date_from: Filter by scheduled_date property. This filter can be
                           used in combination with the scheduled_date_to query parameter to get external
                           transfers scheduled within a specific timeframe. Please use a valid date time format: ISO 8601.
        scheduled_date_to: Filter by scheduled_date property. This filter can be
                         used in combination with the scheduled_date_from query parameter to get external
                         transfers scheduled within a specific timeframe. Please use a valid date time format: ISO 8601.
        beneficiary_ids: Filter by beneficiary_id. You can provide a list of IDs.
        sort_by: Sort by a property. Available options: updated_at:asc, updated_at:desc,
                scheduled_date:asc, scheduled_date:desc.
        page: Returned page of Pagination.
        per_page: Number of external transfers per page of Pagination.
    
    Returns:
        A dictionary containing the list of external transfers for the authenticated organization.
    """
    url = f"{BASE_URL}/external_transfers"

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
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        # response.raise_for_status()
        
        return response.json()

@mcp.tool()
async def retrieve_an_external_transfer(id: str) -> Dict:
    """
    Retrieves the external transfer identified by the id path parameter.
    
    Args:
        id: The ID of the external transfer to retrieve.
              Example: "7b7a5ed6-3983-47b2-89fd-0cf44bd7bef9"
    
    Returns:
        A dictionary containing the external transfer details with the following properties:
        - external_transfer.id: A string identifier (this is a description)
        - external_transfer.slug: A string identifier
        - external_transfer.debit_iban: String representing the organization's bank account IBAN (ISO 13616)
        - external_transfer.debit_amount: String representing the amount debited from your Qonto account
        And other properties as included in the response.
    """
    url = f"{BASE_URL}/external_transfers/{id}"
    
    headers = {
        "Authorization": API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        
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
    
    Note: This endpoint is available until September 31, 2023, for SEPA beneficiaries.
    For SEPA beneficiaries, please use the List SEPA beneficiaries endpoint instead.
    This endpoint remains available for international beneficiaries until a new endpoint supporting
    international beneficiary listing is released.
    
    Args:
        trusted: Beneficiaries can be filtered by their trusted field.
        status: Beneficiaries can be filtered by their status. This filter accepts an array of statuses.
               Available options: pending, validated, declined.
        iban: Beneficiaries can be filtered by their iban. This filter accepts an array of IBANs as value.
        updated_at_from: Beneficiaries can be filtered by their updated_at property. This filter can be used in
                       combination with the updated_at_to query parameter to get beneficiaries updated
                       within a specific timeframe. Please use a valid date time format: ISO 8601.
        updated_at_to: Beneficiaries can be filtered by their updated_at property. This filter can be used in
                     combination with the updated_at_from query parameter to get beneficiaries updated
                     within a specific timeframe. Please use a valid date time format: ISO 8601.
        sort_by: Beneficiaries can be sorted by their updated_at property in 2 possible orders: asc
               (ascending) / desc (descending). Default: updated_at:desc.
               Available options: updated_at:desc, updated_at:asc.
        page: Returned page of Pagination.
        per_page: Number of beneficiaries per page of Pagination.
    
    Returns:
        A dictionary containing the list of beneficiaries for the authenticated organization.
    """
    url = f"{BASE_URL}/beneficiaries"
    
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
    
    headers = {
        "Authorization": API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()

@mcp.tool()
async def retrieve_a_beneficiary(id: str) -> Dict:
    """
    Retrieves the beneficiary identified by the id path parameter.
    
    Note: This endpoint will be deprecated on March 31, 2024. For SEPA beneficiaries,
    please use the Retrieve a SEPA beneficiary endpoint instead. This endpoint 
    remains available for international beneficiaries until a new endpoint supporting
    international beneficiary retrieval is released.
    
    Args:
        id: The ID of the beneficiary to retrieve.
            Example: "e72f4e63-9f27-4415-8781-adb46a859c7f"
    
    Returns:
        A dictionary containing the beneficiary details with the following properties:
        - beneficiary.id: A string identifier
        - beneficiary.name: A string with the beneficiary name
        - beneficiary.status: An enum string with possible values:
          - pending: Beneficiary is created but no Strong Customer Authentication or
                    Transfer has ever been done on this beneficiary.
          - validated: Beneficiary is created and at least one Strong Customer
                      Authentication or Transfer has been done to this beneficiary.
    """
    url = f"{BASE_URL}/beneficiaries/{id}"
    
    headers = {
        "Authorization": API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()

# @mcp.tool()
# async def untrust_a_list_of_beneficiaries(ids: List[str]) -> Dict:
#     """
#     Untrusts up to 400 beneficiaries for the authenticated organization.
    
#     Note: This endpoint will be deprecated on March 31, 2026. For SEPA beneficiaries,
#     please use the Untrust SEPA beneficiaries endpoint instead. This endpoint
#     remains available for international beneficiaries until a new endpoint supporting
#     international beneficiary untrusting is released.
    
#     Args:
#         ids: List of beneficiary IDs to untrust.
#              Example: ["e913bc4e-68db-4ab0-bfab-ca94d37f731b"]
    
#     Returns:
#         A dictionary containing the untrusted beneficiaries with the following properties:
#         - beneficiaries.id: A string identifier for each beneficiary
#         - beneficiaries.name: A string with the beneficiary name
#         - beneficiaries.status: An enum string with possible values:
#           - pending: Beneficiary is created but no Strong Customer Authentication or
#                     Transfer has ever been done on this beneficiary.
#           - validated: Beneficiary is created and at least one Strong Customer
#                       Authentication or Transfer has been done to this beneficiary.
#     """
#     url = f"{BASE_URL}/beneficiaries/untrust"
    
#     headers = {
#         "Authorization": API_KEY,
#         "Content-Type": "application/json"
#     }
    
#     data = {
#         "ids": ids
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.patch(url, json=data, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

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
        iban: Filter by IBAN.
        status: Filter by status.
               Available options: pending, validated, declined.
        trusted: Filter by trusted status.
        page: Page number. Default: 1.
        per_page: Number of items per page. Default: 25.
        sort_by: Sort by property and direction (format is "property:direction").
                Available options: updated_at:desc, updated_at:asc. Default: updated_at:desc.
    
    Returns:
        A dictionary containing the list of SEPA beneficiaries for the authenticated organization
        with the following properties:
        - beneficiaries.id: A string identifier
        - beneficiaries.name: A string with the beneficiary name
        - beneficiaries.activity_tag: An enum string with many available options like ate, fastback, 
          fees, finance, food_and_grocery, etc.
        - beneficiaries.iban: A string containing the IBAN
        - beneficiaries.currency: A string with the currency code
    """
    url = f"{BASE_URL}/sepa/beneficiaries"
    
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
    
    headers = {
        "Authorization": API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()

# @mcp.tool()
# async def retrieve_a_sepa_beneficiary(id: str) -> Dict:
#     """
#     Returns a given SEPA beneficiary by ID.
    
#     Args:
#         id: Beneficiary ID.
    
#     Returns:
#         A dictionary containing the SEPA beneficiary with the following properties:
#         - beneficiary.id: A string identifier (required)
#         - beneficiary.name: A string with the beneficiary name (required)
#         - beneficiary.activity_tag: An enum string (required) with available options:
#           ate, fastback, fees, finance, food_and_grocery, gas_station, hardware_and_equipment,
#           hotel_and_lodging, insurance, it_and_electronics, legal_and_accounting, logistics,
#           manufacturing, marketing, office_rental, office_supply, online_service,
#           other_expense, other_income, other_service, pending, refund, restaurant_and_bar,
#           sales, salary, subscription, tax, transport, treasury_and_interco, utility, voucher
#     """
#     url = f"{BASE_URL}/sepa/beneficiaries/{id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def upload_an_attachment(file_path: str, idempotency_key: Optional[str] = None) -> Dict:
#     """
#     Uploads a single attachment (JPEG, PNG or PDF).
    
#     This operation will enable you to link the uploaded attachment to an
#     external transfer (through POST /v2/external_transfers or POST
#     /v2/external_transfers/checkout).
    
#     In the Qonto app, attachments are files uploaded onto transactions by
#     users. Attachments typically correspond to the invoice or receipt, and
#     are used to justify the transactions from a bookkeeping standpoint.
    
#     Args:
#         file_path: Path to the file to upload (JPEG, PNG or PDF).
#         idempotency_key: Optional. This endpoint supports idempotency for safely retrying 
#                          requests without accidentally performing the same operation twice.
#                          Example: "4668ac59-4e5c-4e51-9d01-fc5c33c79ddd"
    
#     Returns:
#         A dictionary containing information about the uploaded attachment.
#     """
#     url = f"{BASE_URL}/attachments"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     if idempotency_key:
#         headers["X-Qonto-Idempotency-Key"] = idempotency_key
    
#     async with httpx.AsyncClient() as client:
#         with open(file_path, "rb") as file:
#             files = {"file": file}
#             response = await client.post(url, headers=headers, files=files)
#             response.raise_for_status()
            
#             return response.json()

# @mcp.tool()
# async def retrieve_an_attachment(id: str) -> Dict:
#     """
#     Retrieves the attachment identified by the id path parameter.
    
#     In the Qonto app, attachments are files uploaded onto transactions by
#     users. Attachments typically correspond to the invoice or receipt, and
#     are used to justify the transactions from a bookkeeping standpoint.
    
#     You can retrieve the IDs of those attachments inside each
#     transaction object, by calling /v2/transactions.
    
#     Probative attachment is another version of attachment, compliant
#     with PADES standard.
    
#     Note: For security reasons, the url you retrieve for each attachment is only valid
#     for 30 minutes. If you need to download the file after more than 30 minutes,
#     you will need to perform another authenticated call in order to generate a new
#     valid URL.
    
#     Args:
#         id: The ID of the attachment to retrieve.
#             Example: "e7274e43-9f27-4a15-8781-adb44a859c7f"
    
#     Returns:
#         A dictionary containing the attachment details with the following properties:
#         - attachment.id: String identifier of the attachment
#         - attachment.created_at: String representing when the attachment was created
#         - attachment.file_name: String with the name of the file
#         - attachment.file_size: String with the size of the file
#         - attachment.file_content_type: String with the content type of the file
#         - attachment.url: String with the URL to download the file (valid for 30 minutes)
#     """
#     url = f"{BASE_URL}/attachments/{id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()

#         return response.json()

@mcp.tool()
async def list_labels(
    page: Optional[str] = None,
    per_page: Optional[str] = None
) -> Dict:
    """
    Retrieves all the labels for the authenticated organization.
    
    Args:
        page: Returned page of Pagination.
        per_page: Number of labels per page (of Pagination).
    
    Returns:
        A dictionary containing the list of labels for the authenticated organization with:
        - labels: Array of label objects with:
            - labels.id: String that uniquely identifies the label and is used to identify 
                         the label_ids of a transaction (see GET /v2/transactions)
            - labels.name: String containing the name of the label
            - labels.parent_id: String or null that identifies the parent label.
                              A label can be linked to another in order to create lists.
        - meta: Object containing pagination metadata:
            - meta.current_page: Integer representing the current page number
    """
    url = f"{BASE_URL}/labels"

    params = {}
    
    if page:
        params["page"] = page
    
    if per_page:
        params["per_page"] = per_page
    
    headers = {
        "Authorization": API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()

# @mcp.tool()
# async def retrieve_a_label(id: str) -> Dict:
#     """
#     Retrieves the label identified by the id path parameter.
    
#     Args:
#         id: Uniquely identifies the label.
#             Example: "2d96a3fd-1748-4ed4-a590-48066ae9e1cb"
    
#     Returns:
#         A dictionary containing the label details with the following properties:
#         - label.id: String that uniquely identifies the label and is used to identify 
#                    the label_ids of a transaction (see GET /v2/transactions)
#         - label.name: String containing the name of the label
#         - label.parent_id: String or null that identifies the parent label.
#                          A label can be linked to another in order to create lists.
#     """
#     url = f"{BASE_URL}/labels/{id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

@mcp.tool()
async def list_memberships(
    page: Optional[str] = None,
    per_page: Optional[str] = None
) -> Dict:
    """
    Retrieves all the memberships for the authenticated organization.
    
    A member is a user who's been granted access to the Qonto account
    of a company. There is no limit currently to the number of 
    memberships a company can have.
    
    Args:
        page: Returned page.
        per_page: Number of memberships per page (of Pagination).
    
    Returns:
        A dictionary containing the list of memberships for the authenticated organization with:
        - memberships: Array of membership objects with:
            - memberships.id: String that uniquely identifies the membership.
            - memberships.first_name: First name of the member.
            - memberships.last_name: Last name of the member.
            - memberships.role: Role of the member (enum string).
            - Additional fields like nationality, residence_country, etc.
        - meta: Object containing pagination metadata:
            - meta.current_page: Integer representing the current page number
            - meta.total_count: Integer representing the total count of memberships
            - meta.per_page: Integer representing the number of items per page
    """
    url = f"{BASE_URL}/memberships"
    
    params = {}
    
    if page:
        params["page"] = page
    
    if per_page:
        params["per_page"] = per_page
    
    headers = {
        "Authorization": API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()

# @mcp.tool()
# async def retrieve_the_authenticated_organization_and_list_bank_accounts(
#     include_external_accounts: Optional[bool] = False
# ) -> Dict:
#     """
#     Retrieves the details and the list of bank accounts for the authenticated organization.
    
#     The bank account's id or iban will be required to retrieve the list
#     of transactions inside that bank account, using GET /v2/transactions.
    
#     Args:
#         include_external_accounts: By default includes only Qonto accounts. Set to 'true' 
#                                  if you also want to include your connected externals account(s).
#                                  Default: False.
    
#     Returns:
#         A dictionary containing the organization details and its bank accounts with:
#         - organization.id: UUID of the organization.
#         - organization.name: Name of the organization.
#         - organization.slug: Slug based on organization's legal name.
#         - organization.legal_name: Legal name of the organization.
#         - organization.legal_number: Legal identifier of the organization.
#         - And additional fields including bank accounts information:
#           - accounts: Array of account objects each with:
#             - slug: Account identifier
#             - iban: IBAN of the account
#             - bic: BIC of the account
#             - currency: Currency of the account
#             - balance: Current balance
#             - And other account-related details
#     """
#     url = f"{BASE_URL}/organization"
    
#     params = {}
    
#     if include_external_accounts:
#         params["include_external_accounts"] = "true"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, params=params, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def list_attachments_for_a_transaction(
#     id: str, 
#     page: Optional[str] = None,
#     per_page: Optional[str] = None
# ) -> Dict:
#     """
#     Retrieves all the attachments for the transaction identified by the id path parameter.
    
#     In the Qonto app, attachments are files uploaded onto transactions by
#     users. Attachments typically correspond to the invoice or receipt, and
#     are used to justify the transactions from a bookkeeping standpoint.
    
#     You can retrieve the IDs of these attachments inside each
#     transaction object, by calling GET /v2/transactions.
    
#     Probative attachment is another version of attachment, compliant
#     with PADES standard.
    
#     Note: For security reasons, the url you retrieve for each attachment is only valid
#     for 30 minutes. If you need to download the file after more than 30 minutes,
#     you will need to perform another authenticated call in order to generate a new
#     download URL.
    
#     Args:
#         id: Identifies the transaction to retrieve attachments for.
#             Example: "aaa8e6fa-0b4c-4749-9a97-bda8efa9e323"
#         page: Returned page of Pagination.
#         per_page: Number of attachments per page (of Pagination).
    
#     Returns:
#         A dictionary containing the list of attachments for the transaction with:
#         - attachments: Array of attachment objects with:
#             - attachments.id: String identifier of the attachment
#             - attachments.created_at: String representing when the attachment was created
#             - attachments.file_name: String with the name of the file
#             - attachments.file_size: String with the size of the file
#             - attachments.file_content_type: String with the content type of the file
#             - attachments.url: String with the URL to download the file (valid for 30 minutes)
#     """
#     url = f"{BASE_URL}/transactions/{id}/attachments"
    
#     params = {}
    
#     if page:
#         params["page"] = page
    
#     if per_page:
#         params["per_page"] = per_page
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, params=params, headers=headers)
#         response.raise_for_status()
        
#         # Note: URLs in the response might contain \u0026 characters
#         # that need to be replaced with & when used with curl
#         return response.json()

# @mcp.tool()
# async def upload_an_attachment_to_a_transaction(
#     id: str, 
#     file_path: str, 
#     idempotency_key: Optional[str] = None
# ) -> Dict:
#     """
#     Uploads a single attachment (JPEG, PNG or PDF) to the transaction identified by the id path parameter.
    
#     In the Qonto app, attachments are files uploaded onto transactions by
#     users. Attachments typically correspond to the invoice or receipt, and
#     are used to justify the transactions from a bookkeeping standpoint.
    
#     Note: The uploaded file will be processed in the background. This means that the
#     created attachment will not be visible immediately.
    
#     Args:
#         id: Identifies the transaction to which the attachment will be uploaded.
#             Example: "2731e51c-c37f-437f-b018-45efeac89a30"
#         file_path: Path to the file to upload (JPEG, PNG or PDF).
#         idempotency_key: Optional. This API supports idempotency for safely retrying 
#                          requests without accidentally performing the same operation twice.
#                          Example: "4668ac59-4e5c-4e51-9d01-fc5c33c79ddd"
    
#     Returns:
#         A dictionary containing the status of the upload operation.
#     """
#     url = f"{BASE_URL}/transactions/{id}/attachments"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     if idempotency_key:
#         headers["X-Qonto-Idempotency-Key"] = idempotency_key
    
#     async with httpx.AsyncClient() as client:
#         with open(file_path, "rb") as file:
#             files = {"file": file}
#             response = await client.post(url, headers=headers, files=files)
#             response.raise_for_status()

#             try:
#                 return response.json()
#             except:
#                 return {"status": "success", "status_code": response.status_code}

# @mcp.tool()
# async def remove_all_attachments_from_a_transaction(id: str) -> Dict:
#     """
#     Removes all attachments from the transaction identified by the id path parameter.
    
#     In the Qonto app, attachments are files uploaded onto transactions by
#     users. Attachments typically correspond to the invoice or receipt, and
#     are used to justify the transactions from a bookkeeping standpoint.
    
#     Args:
#         id: Identifies the transaction from which all attachments will be removed.
#             Example: "275bad5e-6cb4-409e-88a8-ab4336a3bd57"
    
#     Returns:
#         A dictionary containing the status of the operation.
#     """
#     url = f"{BASE_URL}/transactions/{id}/attachments"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.delete(url, headers=headers)
#         response.raise_for_status()

#         try:
#             return response.json()
#         except:
#             return {"status": "success", "status_code": response.status_code}

# @mcp.tool()
# async def remove_an_attachment_from_a_transaction(
#     transaction_id: str,
#     attachment_id: str
# ) -> None:
#     """
#     Removes a single attachment from the transaction identified by the id path parameter.

#     In the Qonto app, attachments are files uploaded onto transactions by users.
#     Attachments typically correspond to the invoice or receipt, and are used to
#     justify the transactions from a bookkeeping standpoint.

#     Args:
#         client: The HTTP client to use for the request.
#         transaction_id: The ID of the transaction. Example: "644cf847-125e-4ec9-92bb-8d99aee6dbc"
#         attachment_id: The ID of the attachment to remove.

#     Returns:
#         None: Returns nothing on success (204 status code).
#     """
#     url = f"{BASE_URL}/transactions/{transaction_id}/attachments/{attachment_id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.delete(url, headers=headers)
#         response.raise_for_status()
        
#         return None

# @mcp.tool()
# async def list_transactions(
#     bank_account_id: Optional[str] = None,
#     iban: Optional[str] = None,
#     includes: Optional[list[str]] = None,
#     status: Optional[list[str]] = None,
#     updated_at_from: Optional[str] = None,
#     updated_at_to: Optional[str] = None,
#     settled_at_from: Optional[str] = None,
#     settled_at_to: Optional[str] = None,
#     side: Optional[list[str]] = None,
#     operation_type: Optional[list[str]] = None,
#     with_attachments: Optional[bool] = None,
#     sort_by: Optional[str] = None,
#     page: Optional[int] = None,
#     per_page: Optional[int] = None
# ) -> dict:
#     """
#     Retrieves the list of transactions for the bank account identified by the
#     bank_account_id query parameter.
    
#     You can filter (only retrieve the latest transactions) and sort this list by using query parameters.
    
#     Args:
#         bank_account_id: ID of the bank account for which transactions will be retrieved.
#             Example: "9a7f15-c636-7680-a46a-aa656a82c"
#         iban: IBAN of the bank account for which transactions will be retrieved.
#             Example: "FR7611808009101234567890147"
#         includes: Additional resources to include in the response. 
#             Possible values: "labels", "attachments"
#         status: Filter transactions by their status property.
#             Possible values: "pending", "declined", "completed"
#         updated_at_from: Filter transactions by their updated_at property.
#             This filter can be used in combination with updated_at_to to get transactions updated
#             within a specific timeframe. Format uses a valid date-time format (ISO-8601).
#             Example: "2023-01-10T17:37:51.000Z"
#         updated_at_to: Filter transactions by their updated_at property.
#             This filter can be used in combination with updated_at_from to get transactions updated
#             within a specific timeframe. Format uses a valid date-time format (ISO-8601).
#             Example: "2023-01-10T17:37:51.000Z"
#         settled_at_from: Filter transactions by their settled_at property.
#             This filter can be used in combination with settled_at_to to get transactions settled
#             within a specific timeframe. Format uses a valid date-time format (ISO-8601).
#             Example: "2023-01-10T17:37:51.000Z"
#         settled_at_to: Filter transactions by their settled_at property.
#             This filter can be used in combination with settled_at_from to get transactions settled
#             within a specific timeframe. Format uses a valid date-time format (ISO-8601).
#             Example: "2023-01-10T17:37:51.000Z"
#         side: Filter transactions by their side property.
#             Possible values: "debit", "credit"
#         operation_type: Filter transactions by their operation_type property.
#             Example: "transfer_fund","international_wire","transfer"
#         with_attachments: Filter transactions on the presence of one or more attachments.
#         sort_by: Transactions can be sorted by a specific property and order. 
#             Possible values: "updated_at", "settled_at", "amount_cents", "id" | Order: "asc", "desc"
#             Format: "PROPERTY:ORDER"
#         page: Pagination page number.
#         per_page: Number of transactions per page. Pagination.
    
#     Returns:
#         dict: List of transactions for the specified bank account.
#     """
#     url = f"{BASE_URL}/transactions"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     params = {}
#     if bank_account_id:
#         params["bank_account_id"] = bank_account_id
#     if iban:
#         params["iban"] = iban
#     if includes:
#         params["includes[]"] = includes
#     if status:
#         params["status[]"] = status
#     if updated_at_from:
#         params["updated_at_from"] = updated_at_from
#     if updated_at_to:
#         params["updated_at_to"] = updated_at_to
#     if settled_at_from:
#         params["settled_at_from"] = settled_at_from
#     if settled_at_to:
#         params["settled_at_to"] = settled_at_to
#     if side:
#         params["side[]"] = side
#     if operation_type:
#         params["operation_type[]"] = operation_type
#     if with_attachments is not None:
#         params["with_attachments"] = with_attachments
#     if sort_by:
#         params["sort_by"] = sort_by
#     if page:
#         params["page"] = page
#     if per_page:
#         params["per_page"] = per_page

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers, params=params)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def retrieve_a_transaction(
#     transaction_id: str,
#     includes: Optional[list[str]] = None
# ) -> dict:
#     """
#     Retrieves the transaction identified by the id path parameter.
    
#     Args:
#         transaction_id: UUID of the transaction to retrieve.
#             Example: "7b7a5de6-1983-47d2-89fd-bef44dd7bef5"
#         includes: Use this parameter to embed the associated resources (labels, 
#             attachments and/or VAT details) of the transactions in the JSON response.
#             Available options: "vat_details", "labels", "attachments"
    
#     Returns:
#         dict: The transaction object with its details.
#     """
#     url = f"{BASE_URL}/transactions/{transaction_id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     params = {}
#     if includes:
#         params["includes[]"] = includes
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers, params=params)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def create_an_internal_transfer(
#     debit_iban: str,
#     credit_iban: str,
#     reference: str,
#     amount: str,
#     currency: str = "EUR",
#     idempotency_key: str = None
# ) -> dict:
#     """
#     Creates a single instant transfer between 2 bank accounts of the
#     authenticated organization.
    
#     You can obtain the bank accounts' IBAN through the GET /organization endpoint.
    
#     Args:
#         debit_iban: IBAN of account to debit.
#         credit_iban: IBAN of account to credit.
#         reference: Can be used to enter transfer details to further describe the transfer.
#             Maximum reference length is 90 characters.
#         amount: Corresponds to the amount of the transaction in the currency of the bank
#             account. Amounts must be https://www.w3.org/TR/payment-request/#dfn-valid-
#             decimal-monetary-value.
#         currency: Only accepts "EUR".
#         idempotency_key: This endpoint supports idempotency for safely retrying requests 
#             without accidentally performing the same operation twice.
#             Example: "217e57cf-9537-4d62-8deb-57b6d15ebab5"
    
#     Returns:
#         dict: The created internal transfer object.
#     """
#     url = f"{BASE_URL}/internal_transfers"
    
#     headers = {
#         "Authorization": API_KEY,
#         "Content-Type": "application/json"
#     }
    
#     if idempotency_key:
#         headers["X-Qonto-Idempotency-Key"] = idempotency_key
    
#     payload = {
#         "internal_transfer": {
#             "debit_iban": debit_iban,
#             "credit_iban": credit_iban,
#             "reference": reference,
#             "amount": amount,
#             "currency": currency
#         }
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, headers=headers, json=payload)
#         response.raise_for_status()
        
#         return response.json()

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
    Retrieves the list of requests for the authenticated organizations.
    
    You can filter, sort, retrieve a specific request type and sort this
    list by using query parameters.
    
    Args:
        status: Requests can be filtered by their status. Can filter requests on any of the following
            statuses: pending, approved, declined, expired, canceled.
            Example: ["approved", "declined"]
        request_type: Requests can be filtered by their request_type. Can filter requests on any of the
            following statuses: flash_card, which refers to a card proposal sent with a bucket
            limit and a card type of validity. The card reference included after this budget is
            totally spent or after the card has expired. credit_transfer, which refers to a proposal
            for a transfer which adds a monthly budget. Each month can spend that amount when updated
            online. Some cards come with a spending budget which can be automatically updated online
            to prevent any service disruption. sepa_transfer, spend a maximum amount in the
            euro and the following wallets: direct_debit, payroll_invoice.
            Example: ["credit_transfer", "sepa_transfer"]
        created_at_from: Requests can be filtered by their created_at property. Please use a valid date-time
            format (ISO-8601) for searching.
            Example: "2023-01-10T17:37:51.000Z"
        processed_at_from: Requests can be filtered by their processed_at property. Please use a valid date-time
            format (ISO-8601) for searching.
            Example: "2023-01-10T17:37:51.000Z"
        sort_by: Requests can be sorted by a specific property and order. id or Property
            processed_at, created_at, status, id or type. asc (ascending) / desc (descending).
            Available values in the following order: pending, approved, declined, canceled.
        page: Pagination page.
        per_page: Number of requests per page. Pagination.
    
    Returns:
        dict: Returns the list of requests.
    """
    url = f"{BASE_URL}/requests"
    
    headers = {
        "Authorization": API_KEY
    }
    
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
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
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
    Retrieves the list of supplier invoices for the authenticated
    organization.
    
    You can filter (ex: only retrieve the latest supplier invoices) and sort
    this list by using query parameters.
    
    Args:
        client: The httpx AsyncClient to use for the request.
        filter_status: Filter invoices by their status.
        page: Paginated page id.
        per_page: Number of invoices per page (range: 1-100).
        sort_by: Sort invoices by a specific property and order.
                Format: {property}_{asc|desc}.
                Properties: created_at, file_name, supplier_name, payment_date,
                due_date, scheduled_date, total_amount.
                Default is "created_at_desc".
        filter_created_at_from: Filter invoices by their created_at property.
                                Use a valid date time format ISO 8601.
        filter_created_at_to: Filter invoices by their created_at property.
                              Use a valid date time format ISO 8601.
    
    Returns:
        A dictionary containing the list of supplier invoices.
    """
    url = f"{BASE_URL}/supplier_invoices"
    
    headers = {
        "Authorization": API_KEY
    }
    
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
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()

# @mcp.tool()
# async def retrieve_a_supplier_invoice(invoice_id: str) -> dict:
#     """
#     Retrieves the supplier invoice identified by the id path parameter.
    
#     Args:
#         invoice_id: The ID of the supplier invoice.
#             Example: "a9d359b2-aed0-4dce-c87a-cdf4aa5ba54"
    
#     Returns:
#         dict: The supplier invoice object with all its details.
#     """
#     url = f"{BASE_URL}/supplier_invoices/{invoice_id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def create_supplier_invoices(
#     supplier_invoices_file,
#     idempotency_key: str,
#     meta: Optional[str] = None
# ) -> dict:
#     """
#     Creates supplier invoices in bulk for the authenticated organization by
#     uploading files.
    
#     Args:
#         supplier_invoices_file: The file to be uploaded as supplier invoice.
#         idempotency_key: Unique string (one-time) to use a uuid / that identifies an invoice.
#                          This is used by Qonto to prevent performing the same operation twice.
#         meta: Additional metadata for the request.
    
#     Returns:
#         A dictionary containing the supplier invoices created. The endpoint will always return a 200
#         regardless if there are any errors. Clients must ensure to check the "errors" property in
#         order to confirm if all operations were successful.
#     """
#     url = f"{BASE_URL}/supplier_invoices/bulk"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     files = {
#         "supplier_invoices[file]": supplier_invoices_file
#     }
    
#     data = {
#         "supplier_invoices[idempotency_key]": idempotency_key
#     }
    
#     if meta:
#         data["meta"] = meta
    
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             url, 
#             headers=headers, 
#             files=files,
#             data=data
#         )
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def create_a_client_invoice(
#     client_id: str,
#     issue_date: str,
#     due_date: str,
#     number: str,
#     currency: str,
#     payment_method: dict,
#     account_number: dict,
#     items: list,
#     total_vat_amount: str,
#     description: str = None,
#     notes: str = None
# ) -> dict:
#     """
#     Creates a single client invoice for the authenticated organization.
    
#     Do note:
#     - The invoice "status" (top property) of the provided JSON, if the
#       api_version sent in the headers payload is lower than validation
#       error in the /displayable/parameters property.
#     - Italian organizations must have a codeline activated on the
#       Qonto app in order to use this endpoint.
    
#     Args:
#         client_id: Represents the client's ID.
#         issue_date: Represents the date the invoice was issued, in ISO format.
#                    Example: "2022-01-01"
#         due_date: Represents the date the deadline for payment is set by the initiator. The format
#                  should be YYYY-MM-DD.
#         number: Represents the invoice's number.
#                 Example: "INV-001-0001"
#         currency: Represents the invoice's currency for the total amount of the invoice. Currently, only values
#                  allowed are EUR, Polish Złoty (PLN), etc.
#                  Example: "EUR"
#         payment_method: Indicates payment method details for the invoice.
#         account_number: Represents the beneficiary's information like Account Number (IBAN). The format
#                       should be "FR" + digits + bank code (required when your bank type allows IBAN format,
#                       however for QR codes, this field must be provided for the transaction).
#         items: Array of invoice line items.
#         total_vat_amount: Represents the sum of the applicable taxes from all the items in the
#                         invoice table. It indicates in a given currency the product or service being sold.
#         description: Represents the item's description of the product or service being sold. It is advised
#                    to provide the most relevant information about the product, preferably with a maximum of
#                    100 characters. Max: 140 characters.
#         notes: Required for the item's unit. It can be optional field and allows maximum 30 characters
#               for any Italian organization.
    
#     Returns:
#         A dictionary containing the created client invoice.
#     """
#     url = f"{BASE_URL}/client_invoices"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     data = {
#         "client_id": client_id,
#         "issue_date": issue_date,
#         "due_date": due_date,
#         "number": number,
#         "currency": currency,
#         "payment_method": payment_method,
#         "account_number": account_number,
#         "items": items,
#         "total_vat_amount": total_vat_amount
#     }
    
#     if description:
#         data["description"] = description
    
#     if notes:
#         data["notes"] = notes
    
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, headers=headers, json=data)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def list_client_invoices(
#     filter_status: Optional[str] = None,
#     filter_created_at_from: Optional[str] = None,
#     filter_created_at_to: Optional[str] = None,
#     page: Optional[int] = None,
#     per_page: Optional[int] = 1,
#     sort_by: Optional[str] = "created_at_desc"
# ) -> dict:
#     """
#     Retrieves the list of client invoices for the authenticated organization.
    
#     You can filter (ex: only retrieve the latest client invoices) and sort this
#     list by using query parameters.
    
#     Args:
#         filter_status: Filter invoices by their status.
#                       Available options: draft, unpaid, paid, canceled.
#                       - draft: the invoice was created but not validated
#                       - unpaid: the invoice still needs to be published to be paid
#                       - paid: the invoice was created, forwarded to the client, and successfully paid
#                       - canceled: the invoice was created but canceled by the initiator
#         filter_created_at_from: Filter invoices by their created_at property.
#                                This filter can be used in combination with the
#                                filter_created_at_to query parameter to get invoices 
#                                created within a specific timeframe.
#                                Please use a valid date time format ISO 8601.
#         filter_created_at_to: Filter invoices by their created_at property.
#                              This filter can be used in combination with the
#                              filter_created_at_from query parameter to get invoices 
#                              created within a specific timeframe.
#                              Please use a valid date time format ISO 8601.
#         page: Returned page id. For pagination.
#         per_page: Number of invoices per page. Range: 1-100.
#         sort_by: Sort invoices by their created_at property in 2 possible orders:
#                 asc (Ascending) / desc (Descending).
#                 Available options: created_at_desc, created_at_asc
    
#     Returns:
#         A dictionary containing the list of client invoices.
#     """
#     url = f"{BASE_URL}/client_invoices"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     params = {}
#     if filter_status:
#         params["filter[status]"] = filter_status
#     if filter_created_at_from:
#         params["filter[created_at_from]"] = filter_created_at_from
#     if filter_created_at_to:
#         params["filter[created_at_to]"] = filter_created_at_to
#     if page is not None:
#         params["page"] = page
#     if per_page:
#         params["per_page"] = per_page
#     if sort_by:
#         params["sort_by"] = sort_by
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers, params=params)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def retrieve_a_client_invoice(id: str) -> dict:
#     """
#     Retrieves the client invoice identified by the id path parameter.
    
#     Args:
#         id: UUID of the client invoice to retrieve.
    
#     Returns:
#         The client invoice identified by the id path parameter.
#     """
#     url = f"{BASE_URL}/client_invoices/{id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def list_credit_notes(
#     filter_created_at_from: Optional[str] = None,
#     filter_created_at_to: Optional[str] = None,
#     page: Optional[int] = None,
#     per_page: Optional[int] = 1,
#     sort_by: Optional[str] = "created_at_desc"
# ) -> dict:
#     """
#     Retrieves the list of credit notes for the authenticated organization.
    
#     You can filter (ex: only retrieve the latest credit notes) and sort this list
#     by using query parameters.
    
#     Args:
#         filter_created_at_from: Credit notes can be filtered by their created_at property.
#                                Can be use in combination with the filter_created_at_to query
#                                parameter to get credit notes created within a specific timeframe.
#                                Please use a valid date time format ISO 8601 for instance.
#         filter_created_at_to: Credit notes can be filtered by their created_at property.
#                              Can be use in combination with the filter_created_at_from query
#                              parameter to get credit notes created within a specific timeframe.
#                              Please use a valid date time format ISO 8601 for instance.
#         page: Returned page id. For pagination.
#         per_page: Number of credit notes per page. Required range: 1-100.
#         sort_by: Credit notes can be sorted by their created_at property in 2 possible orders:
#                 asc (Ascending) / desc (Descending).
#                 Default is created_at_desc.
    
#     Returns:
#         Returns the list credit notes.
#     """
#     url = f"{BASE_URL}/credit_notes"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     params = {}
#     if filter_created_at_from:
#         params["filter[created_at_from]"] = filter_created_at_from
#     if filter_created_at_to:
#         params["filter[created_at_to]"] = filter_created_at_to
#     if page is not None:
#         params["page"] = page
#     if per_page:
#         params["per_page"] = per_page
#     if sort_by:
#         params["sort_by"] = sort_by
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers, params=params)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def retrieve_a_credit_note(id: str) -> dict:
#     """
#     Retrieves the credit note identified by the id path parameter.
    
#     Args:
#         id: ID of the credit note
    
#     Returns:
#         Returns the credit note identified by the id path parameter.
#     """
#     url = f"{BASE_URL}/credit_notes/{id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def create_a_client(
#     name: str,
#     type: str,
#     email: str,
#     first_name: Optional[str] = None,
#     last_name: Optional[str] = None,
#     vat_number: Optional[str] = None,
#     tax_identification_number: Optional[str] = None,
#     address: Optional[str] = None,
#     city: Optional[str] = None,
#     zip_code: Optional[str] = None,
#     province_code: Optional[str] = None,
#     country_code: Optional[str] = None,
#     billing_address: Optional[dict] = None,
#     delivery_address: Optional[dict] = None
# ) -> dict:
#     """
#     Creates a single client for the authenticated organization.
    
#     Args:
#         name: Represents the name of the client that needs to pay the client invoice. It is required if
#               type is company.
#         type: Describes the client type. 'individual' represents a physical person (a consumer)
#               whereas 'company' or 'freelancer' represent a legal entity. For Italian organizations only,
#               'freelancer' is a legal entity with the name of a person.
#               Available options: individual, company, freelancer
#         email: Represents the e-mail address of the client that needs to pay the invoice, which is
#               displayed in the invoice.
#         first_name: Represents the first name of the client that needs to pay the invoice. It is required if
#                    type is individual or freelancer.
#         last_name: Represents the last name of the client that needs to pay the invoice. It is required if
#                   type is individual or freelancer.
#         vat_number: Represents the Value Added Tax number of the client (Legal entity) that needs to
#                    pay the invoice.
#         tax_identification_number: Represents the Tax Identification Number of the client (a physical person) that needs
#                                   to pay the invoice. It corresponds to the SIREN in FR for companies.
#         address: Represents the address of the client that needs to pay the invoice.
#         city: Represents the city of the client that needs to pay the invoice.
#         zip_code: Represents the zip code of the client that needs to pay the invoice. For client with
#                  Italy as a country, the value must be 5 characters for Italian customers, but value is
#                  required to be 5 characters.
#         province_code: Represents the province code of the client that needs to pay the invoice. It is
#                       required for Italian organizations.
#         country_code: Represents the country code of the client that needs to pay the invoice as a two-
#                      letter country code in ISO 3166-1 format.
#         billing_address: Represents the billing address of the client.
#         delivery_address: Represents the delivery address of the client.
    
#     Returns:
#         A dictionary containing the created client.
#     """
#     url = f"{BASE_URL}/clients"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     data = {
#         "name": name,
#         "type": type,
#         "email": email
#     }
    
#     if first_name:
#         data["first_name"] = first_name
    
#     if last_name:
#         data["last_name"] = last_name
    
#     if vat_number:
#         data["vat_number"] = vat_number
    
#     if tax_identification_number:
#         data["tax_identification_number"] = tax_identification_number
    
#     if address:
#         data["address"] = address
    
#     if city:
#         data["city"] = city
    
#     if zip_code:
#         data["zip_code"] = zip_code
    
#     if province_code:
#         data["province_code"] = province_code
    
#     if country_code:
#         data["country_code"] = country_code
    
#     if billing_address:
#         data["billing_address"] = billing_address
    
#     if delivery_address:
#         data["delivery_address"] = delivery_address
    
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, headers=headers, json=data)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def list_clients(
#     filter_obj: Optional[dict] = None,
#     page: Optional[int] = None,
#     per_page: Optional[int] = 25,
#     sort_by: Optional[str] = "name.asc"
# ) -> dict:
#     """
#     Retrieves the list of clients for the authenticated organization.
    
#     You can filter (ex: only retrieve the latest clients) and sort this list by
#     using query parameters.
    
#     Args:
#         filter_obj: Clients can be filtered based on their tax_identification_number, 
#                   vat_number, or email. The response will return exact and case-insensitive 
#                   matches. For clients with type is individual or freelancer, name consists 
#                   of the concatenation of "first_name" & "-" & "last_name". The value must 
#                   at least contain 2 characters minimum.
#         page: Returned page id. For pagination.
#         per_page: Number of clients per page. Default: 25.
#         sort_by: Clients can be sorted by their created_at or name property in 2 possible orders:
#                 asc (Ascending) / desc (Descending).
#                 Available options: created_at.asc, created_at.desc, name.asc, name.desc
#                 Default is name.asc.
    
#     Returns:
#         Returns the list of clients.
#     """
#     url = f"{BASE_URL}/clients"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     params = {}
#     if filter_obj:
#         params["filter[]"] = filter_obj
#     if page is not None:
#         params["page"] = page
#     if per_page:
#         params["per_page"] = per_page
#     if sort_by:
#         params["sort_by"] = sort_by
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers, params=params)
#         response.raise_for_status()
        
#         return response.json()

# @mcp.tool()
# async def retrieve_a_client(id: str) -> dict:
#     """
#     Retrieves the client identified by the id path parameter.
    
#     Args:
#         id: ID of the client
    
#     Returns:
#         Returns the client identified by the id path parameter.
#     """
#     url = f"{BASE_URL}/clients/{id}"
    
#     headers = {
#         "Authorization": API_KEY
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

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
        bank_account_ids (list[str], optional): Statements can be filtered by their bank_account_id.
            Note: bank_account_ids and ibans are mutually exclusive and cannot be used together.
            Example: ["10F01948-8cB8-4d32-9Ab6-d3fa62baf1c5", "1wT3bx12e0-b818-4dD7-9e4e-ba75e54c021f"]
        
        ibans (list[str], optional): Statements can be filtered by their iban.
            Note: ibans and bank_account_ids are mutually exclusive and cannot be used together.
            Example: ["iban1","iban2","iban3"]
        
        period_from (str, optional): Statements can be filtered by their period. This filter can be used
            in combination with the period_to query parameter to get statements for a specific timeframe.
            Please use a valid date format (ISO 8601 for reference).
            Example: "01-2023"
        
        period_to (str, optional): Statements can be filtered by their period. This filter can be used
            in combination with the period_from query parameter to get statements for a specific timeframe.
            Please use a valid date format (ISO 8601 for reference).
            Example: "12-2023"
        
        page (int, optional): Returned page. Defaults to 1.
            Example: 2
        
        per_page (int, optional): Number of statements per page. Defaults to 100.
            Required range: 1 to 100
            Example: 25
        
        sort_by (str, optional): Statements can be sorted by their period in 2 possible directions:
            asc (ascending) or desc (descending). Defaults to "period:desc".
            Example: "period:asc"
    
    Returns:
        dict: Returns the list of statements.
    """
    url = f"{BASE_URL}/statements"

    headers = {
        "Authorization": API_KEY
    }
    
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
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()

# @mcp.tool()
# async def retrieve_a_statement(id: str) -> dict:
#     """
#     Retrieves the statement identified by the id path parameter.
    
#     Args:
#         id (str): Unique identifier of the statement.
#             Example: "0854c799-6365-4e85-8487-e835290bcee8"
    
#     Returns:
#         dict: The statement data.
#     """
#     url = f"{BASE_URL}/statements/{id}"
#     headers = {
#         "Authorization": API_KEY
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()

@mcp.tool()
async def list_business_accounts(
    page: Optional[int] = 1,
    per_page: Optional[int] = 100
) -> dict:
    """
    Retrieves a list of all business accounts.
    
    You can use this endpoint when you need to display account details
    of all business accounts.
    
    Note on field visibility:
    - Fields available to all users: id, name, status, main, organization_id
    - Fields available to users with Balance Authorization Read: currency, 
      balance, balance_cents, authorized_balance, authorized_balance_cents
    - Owners and admins can access all fields
    
    Args:
        page (int, optional): Page number for pagination. Must be greater than 0.
            Defaults to 1.
        
        per_page (int, optional): Number of business accounts per page. Must be 
            between 1 and 100. Defaults to 100.
    
    Returns:
        dict: List of business accounts retrieved successfully.
    """
    url = f"{BASE_URL}/bank_accounts"
    headers = {
        "Authorization": API_KEY
    }
    
    params = {}
    
    if page != 1:
        params["page"] = page
    
    if per_page != 100:
        params["per_page"] = per_page

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()

# @mcp.tool()
# async def get_a_business_account(id: str) -> dict:
#     """
#     Retrieves detailed information about a specific business account identified by its ID.
    
#     It is useful for retrieving up-to-date information, including the current
#     balance and authorized balance of the account.
    
#     You can use this endpoint when you need to display account details
#     or verify available funds before initiating a transfer.
    
#     Note on field visibility:
#     - Fields available to all users: id, name, status, main, organization_id
#     - Fields available to users with Balance Authorization Read: currency, 
#       balance, balance_cents, authorized_balance, authorized_balance_cents
#     - Owners and admins can access all fields
    
#     Args:
#         id (str): ID of the business account to retrieve
    
#     Returns:
#         dict: Business account retrieved successfully
#     """
#     url = f"{BASE_URL}/bank_accounts/{id}"
#     headers = {
#         "Authorization": API_KEY
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
        
#         return response.json()