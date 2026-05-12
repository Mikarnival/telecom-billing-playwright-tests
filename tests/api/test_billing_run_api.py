import pytest

from api_clients.billing_run_client import BillingRunClient
from api_clients.contract_client import ContractClient
from api_clients.invoice_client import InvoiceClient


@pytest.mark.api
def test_create_billing_run_returns_completed_status(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-06")

    assert response.status in (200, 201)

    billing_run = response.json()

    assert billing_run["status"] == "Completed"


@pytest.mark.api
def test_billing_run_response_contains_required_fields(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-06")

    assert response.status in (200, 201)

    billing_run = response.json()

    assert "billing_run_id" in billing_run
    assert "billing_period" in billing_run
    assert "generated_invoice_ids" in billing_run
    assert "status" in billing_run


@pytest.mark.api
def test_billing_run_generates_invoices_for_active_contracts(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-06")

    assert response.status in (200, 201)

    billing_run = response.json()

    assert billing_run["generated_invoice_ids"] == [
        "INV-202606-CON-5001",
        "INV-202606-CON-5002",
        "INV-202606-CON-5003",
    ]


@pytest.mark.api
def test_generated_invoices_have_unpaid_status(
    billing_run_client: BillingRunClient,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    billing_run_response = billing_run_client.create_billing_run("2026-06")
    billing_run = billing_run_response.json()

    for invoice_id in billing_run["generated_invoice_ids"]:
        invoice_response = invoice_client.get_invoice(invoice_id)

        assert invoice_response.status == 200

        invoice = invoice_response.json()

        assert invoice["status"] == "Unpaid"


@pytest.mark.api
def test_generated_invoices_have_requested_billing_period(
    billing_run_client: BillingRunClient,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    billing_run_response = billing_run_client.create_billing_run("2026-06")
    billing_run = billing_run_response.json()

    for invoice_id in billing_run["generated_invoice_ids"]:
        invoice_response = invoice_client.get_invoice(invoice_id)

        assert invoice_response.status == 200

        invoice = invoice_response.json()

        assert invoice["billing_period"] == "2026-06"


@pytest.mark.api
def test_generated_invoice_amounts_match_plan_prices(
    billing_run_client: BillingRunClient,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    billing_run_response = billing_run_client.create_billing_run("2026-06")
    billing_run = billing_run_response.json()

    expected_amounts_by_plan = {
        "5G Unlimited": 89.00,
        "Fiber Business": 249.00,
        "Business Mobile": 399.00,
    }

    for invoice_id in billing_run["generated_invoice_ids"]:
        invoice_response = invoice_client.get_invoice(invoice_id)

        assert invoice_response.status == 200

        invoice = invoice_response.json()

        assert invoice["amount"] == expected_amounts_by_plan[invoice["plan"]]


@pytest.mark.api
def test_duplicate_billing_run_does_not_create_duplicate_invoices(
    billing_run_client: BillingRunClient,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    first_response = billing_run_client.create_billing_run("2026-06")
    second_response = billing_run_client.create_billing_run("2026-06")

    assert first_response.status in (200, 201)
    assert second_response.status in (200, 201)

    first_billing_run = first_response.json()
    second_billing_run = second_response.json()
    invoices_response = invoice_client.list_invoices()
    invoices = invoices_response.json()
    generated_invoices = [
        invoice
        for invoice in invoices
        if invoice["billing_period"] == "2026-06"
    ]

    assert len(generated_invoices) == len(first_billing_run["generated_invoice_ids"])
    assert second_billing_run["generated_invoice_ids"] == first_billing_run["generated_invoice_ids"]
    assert "no duplicate invoices created" in second_billing_run["message"]


@pytest.mark.api
def test_get_billing_run_by_id_returns_billing_run(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    create_response = billing_run_client.create_billing_run("2026-06")
    created_billing_run = create_response.json()

    response = billing_run_client.get_billing_run("BR-2026-06")

    assert response.status == 200

    billing_run = response.json()

    assert billing_run == created_billing_run


@pytest.mark.api
def test_get_unknown_billing_run_returns_404(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.get_billing_run("BR-2099-12")

    assert response.status == 404

    body = response.json()

    assert "not found" in body["detail"]


@pytest.mark.api
def test_draft_contract_is_ignored_by_billing_run(
    billing_run_client: BillingRunClient,
    contract_client: ContractClient,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    contract_client.create_contract(
        contract_id="CON-9001",
        customer_id="CUST-001",
        plan="5G Unlimited",
    )

    response = billing_run_client.create_billing_run("2026-06")

    assert response.status in (200, 201)

    billing_run = response.json()
    invoices_response = invoice_client.list_invoices()
    invoices = invoices_response.json()
    draft_contract_invoices = [
        invoice
        for invoice in invoices
        if invoice["contract_id"] == "CON-9001"
    ]

    assert "INV-202606-CON-9001" not in billing_run["generated_invoice_ids"]
    assert draft_contract_invoices == []
