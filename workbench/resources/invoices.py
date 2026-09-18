"""
Invoices resource for the Workbench SDK.

Provides methods for managing invoices in Workbench CRM.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional

from workbench.types import (
    Invoice,
    InvoiceItem,
    InvoiceStatus,
    InvoiceWriteStatus,
    ApiResponse,
    ListResponse,
)

if TYPE_CHECKING:
    from workbench.client import WorkbenchClient


def _validate_write_status(status: Optional[InvoiceWriteStatus]) -> None:
    if status is not None and status not in ("draft", "sent", "viewed", "overdue", "cancelled"):
        raise ValueError("Invoice status must be draft, sent, viewed, overdue, or cancelled; payment states are read-only")


class InvoicesResource:
    """
    Invoices resource.

    Example:
        >>> client = WorkbenchClient(api_key="wbk_live_xxx")
        >>>
        >>> # Create an invoice
        >>> invoice = client.invoices.create(
        ...     client_id="client-uuid",
        ...     items=[
        ...         {"description": "Consulting", "quantity": 2, "unit_price": 150}
        ...     ],
        ...     tax_rate=8.5
        ... )
        >>>
        >>> # Send the invoice
        >>> client.invoices.send(invoice["data"]["id"])
    """

    def __init__(self, client: "WorkbenchClient"):
        self._client = client

    def list(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        status: Optional[InvoiceStatus] = None,
        client_id: Optional[str] = None,
    ) -> ListResponse[Invoice]:
        """
        List all invoices.

        Args:
            page: Page number (1-indexed, default: 1)
            per_page: Items per page (1-100, default: 20)
            search: Search by invoice number
            sort: Field to sort by
            order: Sort order ("asc" or "desc")
            status: Filter by status
            client_id: Filter by client ID

        Returns:
            Paginated list of invoices
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "search": search,
            "sort": sort,
            "order": order,
            "status": status,
            "client_id": client_id,
        }
        return self._client.get("/v1/invoices", params=params)  # type: ignore

    def get(self, id: str) -> ApiResponse[Invoice]:
        """
        Get an invoice by ID.

        Args:
            id: Invoice UUID

        Returns:
            Invoice details with line items
        """
        return self._client.get(f"/v1/invoices/{id}")  # type: ignore

    def create(
        self,
        items: List[InvoiceItem],
        client_id: Optional[str] = None,
        job_id: Optional[str] = None,
        status: Optional[InvoiceWriteStatus] = None,
        issue_date: Optional[str] = None,
        due_date: Optional[str] = None,
        tax_rate: Optional[float] = None,
        discount_amount: Optional[float] = None,
        notes: Optional[str] = None,
        terms: Optional[str] = None,
        *,
        discount_type: Optional[Literal["percentage", "fixed"]] = None,
    ) -> ApiResponse[Invoice]:
        """
        Create a new invoice.

        Args:
            items: Line items (required)
            client_id: Client UUID
            job_id: Associated job UUID
            status: Invoice status
            issue_date: Issue date (defaults to today)
            due_date: Payment due date
            tax_rate: Tax rate percentage
            discount_amount: Discount amount
            notes: Notes visible to client
            terms: Payment terms

        Returns:
            Created invoice
        """
        _validate_write_status(status)
        data: Dict[str, Any] = {
            "items": items,
            "client_id": client_id,
            "job_id": job_id,
            "status": status,
            "issue_date": issue_date,
            "due_date": due_date,
            "tax_rate": tax_rate,
            "discount_type": discount_type,
            "discount_amount": discount_amount,
            "notes": notes,
            "terms": terms,
        }
        # Remove None values (except items which is required)
        data = {k: v for k, v in data.items() if v is not None or k == "items"}
        return self._client.post("/v1/invoices", json=data)  # type: ignore

    def update(
        self, id: str, *, status: Optional[InvoiceWriteStatus] = None, **kwargs: Any
    ) -> ApiResponse[Invoice]:
        """
        Update an invoice.

        If items are provided, they will replace all existing line items.

        Args:
            id: Invoice UUID
            **kwargs: Fields to update

        Returns:
            Updated invoice
        """
        _validate_write_status(status)
        # Omission preserves a field; explicit None clears nullable API fields.
        data = dict(kwargs)
        if status is not None:
            data["status"] = status
        return self._client.put(f"/v1/invoices/{id}", json=data)  # type: ignore

    def delete(self, id: str) -> None:
        """
        Delete an invoice.

        Args:
            id: Invoice UUID
        """
        self._client.delete(f"/v1/invoices/{id}")

    def send(self, id: str) -> ApiResponse[Invoice]:
        """
        Mark an invoice as sent.

        Marks a draft invoice as sent and emits its API event.
        This endpoint does not deliver email; use the application's sending workflow.

        Args:
            id: Invoice UUID

        Returns:
            Success response
        """
        return self._client.post(f"/v1/invoices/{id}/send")  # type: ignore
