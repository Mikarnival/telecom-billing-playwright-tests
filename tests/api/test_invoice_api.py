import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.api
@pytest.mark.smoke
def test_health_check_returns_ok(api_context: APIRequestContext) -> None:
    response = api_context.get("/health")

    assert response.status == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.api
@pytest.mark.smoke
def test_list_invoices_returns_default_invoices(
    api_context: APIRequestContext,
    reset_test_data: None,
) -> None:
    response = api_context.get("/api/invoices")

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 3
    assert invoices[0]["invoice_id"] == "INV-1001"
    assert invoices[1]["invoice_id"] == "INV-1002"
    assert invoices[2]["invoice_id"] == "INV-1003"


@pytest.mark.api
def test_search_invoice_by_customer_name(
    api_context: APIRequestContext,
    reset_test_data: None,
) -> None:
    response = api_context.get("/api/invoices?query=Beta")

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 1
    assert invoices[0]["invoice_id"] == "INV-1002"
    assert invoices[0]["customer_name"] == "Beta Telecom"


@pytest.mark.api
def test_filter_unpaid_invoices(
    api_context: APIRequestContext,
    reset_test_data: None,
) -> None:
    response = api_context.get("/api/invoices?status=Unpaid")

    assert response.status == 200

    invoices = response.json()

    assert len(invoices) == 1
    assert invoices[0]["invoice_id"] == "INV-1002"
    assert invoices[0]["status"] == "Unpaid"


@pytest.mark.api
def test_get_invoice_by_id(
    api_context: APIRequestContext,
    reset_test_data: None,
) -> None:
    response = api_context.get("/api/invoices/INV-1002")

    assert response.status == 200

    invoice = response.json()

    assert invoice["invoice_id"] == "INV-1002"
    assert invoice["customer_name"] == "Beta Telecom"
    assert invoice["amount"] == 249.00
    assert invoice["status"] == "Unpaid"


@pytest.mark.api
def test_get_unknown_invoice_returns_404(api_context: APIRequestContext) -> None:
    response = api_context.get("/api/invoices/INV-9999")

    assert response.status == 404

    body = response.json()

    assert "not found" in body["detail"]


@pytest.mark.api
@pytest.mark.smoke
def test_mark_invoice_as_paid_through_api(
    api_context: APIRequestContext,
    reset_test_data: None,
) -> None:
    response = api_context.patch("/api/invoices/INV-1002/pay")

    assert response.status == 200

    invoice = response.json()

    assert invoice["invoice_id"] == "INV-1002"
    assert invoice["status"] == "Paid"

    get_response = api_context.get("/api/invoices/INV-1002")
    updated_invoice = get_response.json()

    assert updated_invoice["status"] == "Paid"