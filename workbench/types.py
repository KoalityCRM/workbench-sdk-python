"""
Type definitions for the Workbench SDK.

These types mirror the API response structures and provide
full type safety when working with the Workbench API.
"""

from datetime import datetime
from typing import Any, Generic, List, Literal, Optional, TypedDict, TypeVar
from typing_extensions import NotRequired

# ===========================================
# GENERIC TYPES
# ===========================================

T = TypeVar("T")


class Pagination(TypedDict):
    """Pagination information for list responses."""

    page: int
    per_page: int
    total: int
    total_pages: int
    has_more: bool


class ResponseMeta(TypedDict):
    """Standard API response metadata."""

    request_id: str
    timestamp: str


class ApiResponse(TypedDict, Generic[T]):
    """Standard API response wrapper for single items."""

    data: T
    meta: ResponseMeta


class ListResponse(TypedDict, Generic[T]):
    """Standard API response wrapper for lists."""

    data: List[T]
    meta: ResponseMeta
    pagination: Pagination


# ===========================================
# CLIENT TYPES
# ===========================================

ClientStatus = Literal["active", "inactive", "lead", "prospect"]


class Client(TypedDict):
    """Client record."""

    id: str
    business_id: str
    first_name: str
    last_name: Optional[str]
    company: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    status: ClientStatus
    source: Optional[str]
    notes: Optional[str]
    tags: Optional[List[str]]
    next_contact_date: Optional[str]
    ask_for_review: Optional[bool]
    created_at: str
    updated_at: str


class CreateClientParams(TypedDict):
    """Parameters for creating a client."""

    first_name: str
    last_name: NotRequired[Optional[str]]
    company: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    phone: NotRequired[Optional[str]]
    status: NotRequired[ClientStatus]
    source: NotRequired[Optional[str]]
    notes: NotRequired[Optional[str]]
    tags: NotRequired[Optional[List[str]]]


class UpdateClientParams(TypedDict, total=False):
    """Parameters for updating a client."""

    first_name: str
    last_name: Optional[str]
    company: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    status: ClientStatus
    source: Optional[str]
    notes: Optional[str]
    tags: Optional[List[str]]
    next_contact_date: Optional[str]
    ask_for_review: Optional[bool]


class ListClientsParams(TypedDict, total=False):
    """Parameters for listing clients."""

    page: int
    per_page: int
    search: str
    sort: str
    order: Literal["asc", "desc"]
    status: ClientStatus


# ===========================================
# INVOICE TYPES
# ===========================================

InvoiceStatus = Literal["draft", "sent", "viewed", "partial", "paid", "overdue", "cancelled"]


class InvoiceItem(TypedDict):
    """Invoice line item."""

    id: NotRequired[str]
    description: str
    quantity: float
    unit_price: float
    sort_order: NotRequired[int]


class Invoice(TypedDict):
    """Invoice record."""

    id: str
    business_id: str
    client_id: Optional[str]
    job_id: Optional[str]
    invoice_number: str
    status: InvoiceStatus
    issue_date: str
    due_date: Optional[str]
    subtotal: float
    tax_rate: Optional[float]
    tax_amount: Optional[float]
    discount_amount: Optional[float]
    total: float
    amount_paid: float
    notes: Optional[str]
    terms: Optional[str]
    items: List[InvoiceItem]
    client: NotRequired[Client]
    created_at: str
    updated_at: str


class CreateInvoiceParams(TypedDict):
    """Parameters for creating an invoice."""

    items: List[InvoiceItem]
    client_id: NotRequired[Optional[str]]
    job_id: NotRequired[Optional[str]]
    status: NotRequired[InvoiceStatus]
    issue_date: NotRequired[str]
    due_date: NotRequired[Optional[str]]
    tax_rate: NotRequired[Optional[float]]
    discount_amount: NotRequired[Optional[float]]
    notes: NotRequired[Optional[str]]
    terms: NotRequired[Optional[str]]


class UpdateInvoiceParams(TypedDict, total=False):
    """Parameters for updating an invoice."""

    client_id: Optional[str]
    job_id: Optional[str]
    status: InvoiceStatus
    issue_date: str
    due_date: Optional[str]
    tax_rate: Optional[float]
    discount_amount: Optional[float]
    notes: Optional[str]
    terms: Optional[str]
    items: List[InvoiceItem]


class ListInvoicesParams(TypedDict, total=False):
    """Parameters for listing invoices."""

    page: int
    per_page: int
    search: str
    sort: str
    order: Literal["asc", "desc"]
    status: InvoiceStatus
    client_id: str


# ===========================================
# QUOTE TYPES
# ===========================================

QuoteStatus = Literal["draft", "sent", "viewed", "approved", "rejected", "expired", "converted"]


class QuoteItem(TypedDict):
    """Quote line item."""

    id: NotRequired[str]
    description: str
    quantity: float
    unit_price: float
    sort_order: NotRequired[int]


class Quote(TypedDict):
    """Quote record."""

    id: str
    business_id: str
    client_id: Optional[str]
    job_id: Optional[str]
    quote_number: str
    status: QuoteStatus
    issue_date: str
    valid_until: Optional[str]
    subtotal: float
    tax_rate: Optional[float]
    tax_amount: Optional[float]
    discount_amount: Optional[float]
    total: float
    notes: Optional[str]
    terms: Optional[str]
    items: List[QuoteItem]
    client: NotRequired[Client]
    created_at: str
    updated_at: str


class CreateQuoteParams(TypedDict):
    """Parameters for creating a quote."""

    items: List[QuoteItem]
    client_id: NotRequired[Optional[str]]
    job_id: NotRequired[Optional[str]]
    status: NotRequired[QuoteStatus]
    issue_date: NotRequired[str]
    valid_until: NotRequired[Optional[str]]
    tax_rate: NotRequired[Optional[float]]
    discount_amount: NotRequired[Optional[float]]
    notes: NotRequired[Optional[str]]
    terms: NotRequired[Optional[str]]


class UpdateQuoteParams(TypedDict, total=False):
    """Parameters for updating a quote."""

    client_id: Optional[str]
    job_id: Optional[str]
    status: QuoteStatus
    issue_date: str
    valid_until: Optional[str]
    tax_rate: Optional[float]
    discount_amount: Optional[float]
    notes: Optional[str]
    terms: Optional[str]
    items: List[QuoteItem]


class ListQuotesParams(TypedDict, total=False):
    """Parameters for listing quotes."""

    page: int
    per_page: int
    search: str
    sort: str
    order: Literal["asc", "desc"]
    status: QuoteStatus
    client_id: str


# ===========================================
# JOB TYPES
# ===========================================

JobStatus = Literal["pending", "scheduled", "in_progress", "completed", "cancelled", "on_hold"]
JobPriority = Literal["low", "medium", "high", "urgent"]


class Job(TypedDict):
    """Job record."""

    id: str
    business_id: str
    client_id: Optional[str]
    title: str
    description: Optional[str]
    status: JobStatus
    priority: JobPriority
    scheduled_start: Optional[str]
    scheduled_end: Optional[str]
    actual_start: Optional[str]
    actual_end: Optional[str]
    estimated_duration: Optional[int]
    address_id: Optional[str]
    notes: Optional[str]
    client: NotRequired[Client]
    created_at: str
    updated_at: str


class CreateJobParams(TypedDict):
    """Parameters for creating a job."""

    title: str
    client_id: NotRequired[Optional[str]]
    description: NotRequired[Optional[str]]
    status: NotRequired[JobStatus]
    priority: NotRequired[JobPriority]
    scheduled_start: NotRequired[Optional[str]]
    scheduled_end: NotRequired[Optional[str]]
    estimated_duration: NotRequired[Optional[int]]
    address_id: NotRequired[Optional[str]]
    notes: NotRequired[Optional[str]]


class UpdateJobParams(TypedDict, total=False):
    """Parameters for updating a job."""

    client_id: Optional[str]
    title: str
    description: Optional[str]
    status: JobStatus
    priority: JobPriority
    scheduled_start: Optional[str]
    scheduled_end: Optional[str]
    actual_start: Optional[str]
    actual_end: Optional[str]
    estimated_duration: Optional[int]
    address_id: Optional[str]
    notes: Optional[str]


class ListJobsParams(TypedDict, total=False):
    """Parameters for listing jobs."""

    page: int
    per_page: int
    search: str
    sort: str
    order: Literal["asc", "desc"]
    status: JobStatus
    priority: JobPriority
    client_id: str


# ===========================================
# SERVICE REQUEST TYPES
# ===========================================

ServiceRequestStatus = Literal[
    "new", "reviewing", "scheduled", "completed", "cancelled", "declined"
]
ServiceRequestPriority = Literal["low", "medium", "high", "urgent"]


class ServiceRequest(TypedDict):
    """Service request record."""

    id: str
    business_id: str
    client_id: Optional[str]
    title: str
    description: Optional[str]
    status: ServiceRequestStatus
    source: Optional[str]
    priority: Optional[ServiceRequestPriority]
    requested_date: Optional[str]
    preferred_time: Optional[str]
    address: Optional[str]
    contact_name: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    notes: Optional[str]
    client: NotRequired[Client]
    created_at: str
    updated_at: str


class CreateServiceRequestParams(TypedDict):
    """Parameters for creating a service request."""

    title: str
    client_id: NotRequired[Optional[str]]
    description: NotRequired[Optional[str]]
    status: NotRequired[ServiceRequestStatus]
    source: NotRequired[Optional[str]]
    priority: NotRequired[Optional[ServiceRequestPriority]]
    requested_date: NotRequired[Optional[str]]
    preferred_time: NotRequired[Optional[str]]
    address: NotRequired[Optional[str]]
    contact_name: NotRequired[Optional[str]]
    contact_email: NotRequired[Optional[str]]
    contact_phone: NotRequired[Optional[str]]
    notes: NotRequired[Optional[str]]


class UpdateServiceRequestParams(TypedDict, total=False):
    """Parameters for updating a service request."""

    client_id: Optional[str]
    title: str
    description: Optional[str]
    status: ServiceRequestStatus
    source: Optional[str]
    priority: Optional[ServiceRequestPriority]
    requested_date: Optional[str]
    preferred_time: Optional[str]
    address: Optional[str]
    contact_name: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    notes: Optional[str]


class ListServiceRequestsParams(TypedDict, total=False):
    """Parameters for listing service requests."""

    page: int
    per_page: int
    search: str
    sort: str
    order: Literal["asc", "desc"]
    status: ServiceRequestStatus
    priority: ServiceRequestPriority
    client_id: str


# ===========================================
# WEBHOOK TYPES
# ===========================================

WebhookEvent = Literal[
    "client.created",
    "client.updated",
    "client.deleted",
    "invoice.created",
    "invoice.sent",
    "invoice.paid",
    "invoice.overdue",
    "quote.created",
    "quote.sent",
    "quote.accepted",
    "quote.rejected",
    "job.created",
    "job.status_changed",
    "job.completed",
    "service_request.created",
    "service_request.assigned",
]


class Webhook(TypedDict):
    """Webhook subscription."""

    id: str
    business_id: str
    name: str
    url: str
    events: List[WebhookEvent]
    secret: str
    is_active: bool
    created_at: str
    updated_at: str


class WebhookDelivery(TypedDict):
    """Webhook delivery record."""

    id: str
    webhook_id: str
    event_type: WebhookEvent
    payload: dict[str, Any]
    response_status: Optional[int]
    response_body: Optional[str]
    attempt_count: int
    next_retry_at: Optional[str]
    delivered_at: Optional[str]
    failed_at: Optional[str]
    created_at: str


class CreateWebhookParams(TypedDict):
    """Parameters for creating a webhook."""

    name: str
    url: str
    events: List[WebhookEvent]


class UpdateWebhookParams(TypedDict, total=False):
    """Parameters for updating a webhook."""

    name: str
    url: str
    events: List[WebhookEvent]
    is_active: bool


class ListWebhookDeliveriesParams(TypedDict, total=False):
    """Parameters for listing webhook deliveries."""

    page: int
    per_page: int
    event_type: WebhookEvent
