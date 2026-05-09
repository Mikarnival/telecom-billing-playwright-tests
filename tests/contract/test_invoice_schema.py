import pytest

from api_clients.invoice_client import InvoiceClient


@pytest.mark.contract
def test_invoice_response_contains_required_fields(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.get_invoice("INV-1002")

    assert response.status == 200

    invoice = response.json()

    required_fields = {
        "invoice_id",
        "customer_id",
        "customer_name",
        "contract_id",
        "plan",
        "amount",
        "status",
        "billing_period",
    }

    assert required_fields.issubset(invoice.keys())


@pytest.mark.contract
def test_invoice_response_field_types(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.get_invoice("INV-1002")

    assert response.status == 200

    invoice = response.json()

    assert isinstance(invoice["invoice_id"], str)
    assert isinstance(invoice["customer_id"], str)
    assert isinstance(invoice["customer_name"], str)
    assert isinstance(invoice["contract_id"], str)
    assert isinstance(invoice["plan"], str)
    assert isinstance(invoice["amount"], float | int)
    assert isinstance(invoice["status"], str)
    assert isinstance(invoice["billing_period"], str)


@pytest.mark.contract
def test_invoice_status_has_valid_value(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.get_invoice("INV-1002")

    assert response.status == 200

    invoice = response.json()

    allowed_statuses = {"Paid", "Unpaid", "Overdue"}

    assert invoice["status"] in allowed_statuses