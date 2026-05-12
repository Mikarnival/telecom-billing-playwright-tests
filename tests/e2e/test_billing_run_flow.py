import pytest
from playwright.sync_api import Page

from api_clients.billing_run_client import BillingRunClient
from api_clients.invoice_client import InvoiceClient
from pages.billing_dashboard_page import BillingDashboardPage


@pytest.mark.e2e
def test_run_monthly_billing_from_ui_and_verify_by_api(
    page: Page,
    frontend_base_url: str,
    billing_run_client: BillingRunClient,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.run_monthly_billing("2026-09")

    dashboard.expect_billing_success_message("BR-2026-09")

    billing_run_response = billing_run_client.get_billing_run("BR-2026-09")

    assert billing_run_response.status == 200

    billing_run = billing_run_response.json()

    assert billing_run["billing_run_id"] == "BR-2026-09"
    assert billing_run["status"] == "Completed"
    assert len(billing_run["generated_invoice_ids"]) > 0

    for invoice_id in billing_run["generated_invoice_ids"]:
        invoice_response = invoice_client.get_invoice(invoice_id)

        assert invoice_response.status == 200

        invoice = invoice_response.json()

        assert invoice["status"] == "Unpaid"
        assert invoice["billing_period"] == "2026-09"

    first_generated_invoice_id = billing_run["generated_invoice_ids"][0]

    dashboard.expect_invoice_visible(first_generated_invoice_id)
    dashboard.expect_invoice_risk(first_generated_invoice_id, "Medium Risk")
