import pytest

from api_clients.invoice_client import InvoiceClient


@pytest.mark.api
@pytest.mark.smoke
def test_health_check_returns_ok(
    invoice_client: InvoiceClient,
) -> None:
    response = invoice_client.health_check()

    assert response.status == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.api
@pytest.mark.smoke
def test_list_invoices_returns_default_invoices(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.list_invoices()

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 3
    assert invoices[0]["invoice_id"] == "INV-1001"
    assert invoices[1]["invoice_id"] == "INV-1002"
    assert invoices[2]["invoice_id"] == "INV-1003"


@pytest.mark.api
def test_search_invoice_by_customer_name(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.search_invoices("Beta")

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 1
    assert invoices[0]["invoice_id"] == "INV-1002"
    assert invoices[0]["customer_name"] == "Beta Telecom"
    assert invoices[0]["status"] == "Unpaid"


@pytest.mark.api
def test_filter_unpaid_invoices(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.filter_invoices_by_status("Unpaid")

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 1
    assert invoices[0]["invoice_id"] == "INV-1002"
    assert invoices[0]["status"] == "Unpaid"


@pytest.mark.api
def test_filter_paid_invoices(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.filter_invoices_by_status("Paid")

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 1
    assert invoices[0]["invoice_id"] == "INV-1001"
    assert invoices[0]["status"] == "Paid"


@pytest.mark.api
def test_filter_overdue_invoices(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.filter_invoices_by_status("Overdue")

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 1
    assert invoices[0]["invoice_id"] == "INV-1003"
    assert invoices[0]["status"] == "Overdue"


@pytest.mark.api
def test_get_invoice_by_id(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.get_invoice("INV-1002")

    assert response.status == 200

    invoice = response.json()

    assert invoice["invoice_id"] == "INV-1002"
    assert invoice["customer_id"] == "CUST-002"
    assert invoice["customer_name"] == "Beta Telecom"
    assert invoice["contract_id"] == "CON-5002"
    assert invoice["plan"] == "Fiber Business"
    assert invoice["amount"] == 249.00
    assert invoice["status"] == "Unpaid"
    assert invoice["billing_period"] == "2026-05"


@pytest.mark.api
def test_get_unknown_invoice_returns_404(
    invoice_client: InvoiceClient,
) -> None:
    response = invoice_client.get_invoice("INV-9999")

    assert response.status == 404

    body = response.json()

    assert "not found" in body["detail"]


@pytest.mark.api
@pytest.mark.smoke
def test_mark_invoice_as_paid_through_api(
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = invoice_client.mark_as_paid("INV-1002")

    assert response.status == 200

    invoice = response.json()

    assert invoice["invoice_id"] == "INV-1002"
    assert invoice["status"] == "Paid"

    get_response = invoice_client.get_invoice("INV-1002")
    updated_invoice = get_response.json()

    assert updated_invoice["invoice_id"] == "INV-1002"
    assert updated_invoice["status"] == "Paid"


@pytest.mark.api
def test_mark_unknown_invoice_as_paid_returns_404(
    invoice_client: InvoiceClient,
) -> None:
    response = invoice_client.mark_as_paid("INV-9999")

    assert response.status == 404

    body = response.json()

    assert "not found" in body["detail"]