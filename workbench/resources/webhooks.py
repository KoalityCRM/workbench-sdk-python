"""
Webhooks resource for the Workbench SDK.

Provides methods for managing webhook subscriptions in Workbench CRM.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from workbench.types import (
    Webhook,
    WebhookDelivery,
    WebhookEvent,
    ApiResponse,
    ListResponse,
)

if TYPE_CHECKING:
    from workbench.client import WorkbenchClient


class WebhooksResource:
    """
    Webhooks resource.

    Example:
        >>> client = WorkbenchClient(api_key="wbk_live_xxx")
        >>>
        >>> # Create a webhook
        >>> webhook = client.webhooks.create(
        ...     name="Invoice Notifications",
        ...     url="https://example.com/webhooks/workbench",
        ...     events=["invoice.created", "invoice.paid"]
        ... )
        >>>
        >>> # Store the secret securely!
        >>> print(f"Webhook secret: {webhook['data']['secret']}")
    """

    def __init__(self, client: "WorkbenchClient"):
        self._client = client

    def list(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> ListResponse[Webhook]:
        """
        List all webhooks.

        Args:
            page: Page number (1-indexed, default: 1)
            per_page: Items per page (1-100, default: 20)

        Returns:
            Paginated list of webhooks
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }
        return self._client.get("/v1/webhooks", params=params)  # type: ignore

    def get(self, id: str) -> ApiResponse[Webhook]:
        """
        Get a webhook by ID.

        Args:
            id: Webhook UUID

        Returns:
            Webhook details
        """
        return self._client.get(f"/v1/webhooks/{id}")  # type: ignore

    def create(
        self,
        name: str,
        url: str,
        events: List[WebhookEvent],
    ) -> ApiResponse[Webhook]:
        """
        Create a new webhook.

        The webhook secret is returned in the response - store it securely
        to verify webhook signatures.

        Args:
            name: Webhook name
            url: Webhook endpoint URL
            events: List of events to subscribe to

        Returns:
            Created webhook (includes secret)
        """
        data: Dict[str, Any] = {
            "name": name,
            "url": url,
            "events": events,
        }
        return self._client.post("/v1/webhooks", json=data)  # type: ignore

    def update(
        self,
        id: str,
        name: Optional[str] = None,
        url: Optional[str] = None,
        events: Optional[List[WebhookEvent]] = None,
        is_active: Optional[bool] = None,
    ) -> ApiResponse[Webhook]:
        """
        Update a webhook.

        Args:
            id: Webhook UUID
            name: New webhook name
            url: New webhook URL
            events: New list of events
            is_active: Whether the webhook is active

        Returns:
            Updated webhook
        """
        data: Dict[str, Any] = {
            "name": name,
            "url": url,
            "events": events,
            "is_active": is_active,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self._client.put(f"/v1/webhooks/{id}", json=data)  # type: ignore

    def delete(self, id: str) -> None:
        """
        Delete a webhook.

        Args:
            id: Webhook UUID
        """
        self._client.delete(f"/v1/webhooks/{id}")

    def list_deliveries(
        self,
        webhook_id: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        event_type: Optional[WebhookEvent] = None,
    ) -> ListResponse[WebhookDelivery]:
        """
        List webhook deliveries.

        Args:
            webhook_id: Webhook UUID
            page: Page number (1-indexed, default: 1)
            per_page: Items per page (1-100, default: 20)
            event_type: Filter by event type

        Returns:
            Paginated list of delivery attempts
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "event_type": event_type,
        }
        return self._client.get(f"/v1/webhooks/{webhook_id}/deliveries", params=params)  # type: ignore

    def test(self, id: str) -> ApiResponse[Dict[str, str]]:
        """
        Send a test webhook.

        Args:
            id: Webhook UUID

        Returns:
            Test delivery result
        """
        return self._client.post(f"/v1/webhooks/{id}/test")  # type: ignore
