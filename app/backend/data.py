from copy import deepcopy
from typing import Any


INITIAL_INVOICES: list[dict[str, Any]] = [
    {
        "invoice_id": "INV-1001",
        "customer_id": "CUST-001",
        "customer_name": "Alice Mobile",
        "contract_id": "CON-5001",
        "plan": "5G Unlimited",
        "amount": 89.00,
        "status": "Paid",
        "billing_period": "2026-05",
    },
    {
        "invoice_id": "INV-1002",
        "customer_id": "CUST-002",
        "customer_name": "Beta Telecom",
        "contract_id": "CON-5002",
        "plan": "Fiber Business",
        "amount": 249.00,
        "status": "Unpaid",
        "billing_period": "2026-05",
    },
    {
        "invoice_id": "INV-1003",
        "customer_id": "CUST-003",
        "customer_name": "Delta GmbH",
        "contract_id": "CON-5003",
        "plan": "Business Mobile",
        "amount": 399.00,
        "status": "Overdue",
        "billing_period": "2026-05",
    },
]


invoices: list[dict[str, Any]] = deepcopy(INITIAL_INVOICES)


def reset_data() -> None:
    """
    Reset mock data to its initial state.
    Useful for tests, so each test starts from the same data.
    """
    global invoices
    invoices = deepcopy(INITIAL_INVOICES)


def get_all_invoices() -> list[dict[str, Any]]:
    return invoices


def get_invoice_by_id(invoice_id: str) -> dict[str, Any] | None:
    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return None


def search_invoices(query: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
    result = invoices

    if query:
        normalized_query = query.lower()
        result = [
            invoice
            for invoice in result
            if normalized_query in invoice["invoice_id"].lower()
            or normalized_query in invoice["customer_name"].lower()
            or normalized_query in invoice["customer_id"].lower()
        ]

    if status:
        normalized_status = status.lower()
        result = [
            invoice
            for invoice in result
            if invoice["status"].lower() == normalized_status
        ]

    return result


def mark_invoice_as_paid(invoice_id: str) -> dict[str, Any] | None:
    invoice = get_invoice_by_id(invoice_id)

    if invoice is None:
        return None

    invoice["status"] = "Paid"
    return invoice