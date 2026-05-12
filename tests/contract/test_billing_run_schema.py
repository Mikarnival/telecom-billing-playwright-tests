import pytest

from api_clients.billing_run_client import BillingRunClient
from api_clients.invoice_client import InvoiceClient


@pytest.mark.contract
def test_billing_run_response_contains_required_fields(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-07")

    assert response.status in (200, 201)

    billing_run = response.json()

    required_fields = {
        "billing_run_id",
        "billing_period",
        "generated_invoice_ids",
        "status",
    }

    assert required_fields.issubset(billing_run.keys())


@pytest.mark.contract
def test_billing_run_response_field_types(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-07")

    assert response.status in (200, 201)

    billing_run = response.json()

    assert isinstance(billing_run["billing_run_id"], str)
    assert isinstance(billing_run["billing_period"], str)
    assert isinstance(billing_run["generated_invoice_ids"], list)
    assert isinstance(billing_run["status"], str)


@pytest.mark.contract
def test_billing_run_status_has_valid_value(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-07")

    assert response.status in (200, 201)

    billing_run = response.json()

    allowed_statuses = {"Completed"}

    assert billing_run["status"] in allowed_statuses


@pytest.mark.contract
def test_generated_invoice_ids_contains_invoice_ids_as_strings(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-07")

    assert response.status in (200, 201)

    billing_run = response.json()

    assert len(billing_run["generated_invoice_ids"]) > 0

    for invoice_id in billing_run["generated_invoice_ids"]:
        assert isinstance(invoice_id, str)
        assert invoice_id.startswith("INV-")


@pytest.mark.contract
def test_each_generated_invoice_id_can_be_fetched(
    billing_run_client: BillingRunClient,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    response = billing_run_client.create_billing_run("2026-07")

    assert response.status in (200, 201)

    billing_run = response.json()

    for invoice_id in billing_run["generated_invoice_ids"]:
        invoice_response = invoice_client.get_invoice(invoice_id)

        assert invoice_response.status == 200

        invoice = invoice_response.json()

        assert invoice["invoice_id"] == invoice_id


@pytest.mark.contract
def test_duplicate_billing_run_response_contains_required_fields(
    billing_run_client: BillingRunClient,
    reset_test_data: None,
) -> None:
    billing_run_client.create_billing_run("2026-07")
    response = billing_run_client.create_billing_run("2026-07")

    assert response.status in (200, 201)

    billing_run = response.json()

    required_fields = {
        "billing_run_id",
        "billing_period",
        "generated_invoice_ids",
        "status",
    }

    assert required_fields.issubset(billing_run.keys())

    if "message" in billing_run:
        assert isinstance(billing_run["message"], str)
