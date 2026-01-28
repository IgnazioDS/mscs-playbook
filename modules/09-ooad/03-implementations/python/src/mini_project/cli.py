"""Mini-project CLI: place order and capture payment."""

from __future__ import annotations

from src.mini_project.application.commands import CapturePaymentCommand, PlaceOrderCommand
from src.mini_project.application.services import OrderService
from src.mini_project.domain.entities import LineItem, Money
from src.mini_project.domain.policies import PercentageDiscount
from src.mini_project.infrastructure.notifier import AuditLogSubscriber, EmailNotifier, EventBus
from src.mini_project.infrastructure.payments import PaymentProcessorFactory
from src.mini_project.infrastructure.repositories import OrderRepository


def main() -> None:
    repo = OrderRepository()
    bus = EventBus()
    payments = PaymentProcessorFactory()
    service = OrderService(repo, bus, payments)

    emails: list[str] = []
    audits: list[str] = []
    email_notifier = EmailNotifier(emails)
    audit_notifier = AuditLogSubscriber(audits)
    bus.subscribe("OrderPlaced", email_notifier.handle)
    bus.subscribe("PaymentCaptured", email_notifier.handle)
    bus.subscribe("PaymentCaptured", audit_notifier.handle)

    items = [
        LineItem("sku-1", "Widget", Money(1500), 2),
        LineItem("sku-2", "Cable", Money(500), 1),
    ]
    discount = PercentageDiscount(0.1)

    place_cmd = PlaceOrderCommand(service, "cust-1", items, discount, "stripe")
    order_id = place_cmd.execute()

    capture_cmd = CapturePaymentCommand(service, order_id, "stripe")
    receipt = capture_cmd.execute()

    print("receipt:")
    print(f"  order_id: {receipt.order_id}")
    print(f"  total: {receipt.total}")
    print(f"  status: {receipt.status}")
    print(f"  payment_provider: {receipt.provider}")
    print(f"  notifications_sent: {len(emails)}")
    print(f"  audit_logs: {len(audits)}")


if __name__ == "__main__":
    main()
