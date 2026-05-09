import pytest
from playwright.sync_api import Page

from api_clients.invoice_client import InvoiceClient
from pages.billing_dashboard_page import BillingDashboardPage


@pytest.mark.e2e
@pytest.mark.smoke
def test_mark_invoice_as_paid_from_ui_and_verify_by_api(
    page: Page,
    frontend_base_url: str,
    invoice_client: InvoiceClient,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.expect_invoice_status("INV-1002", "Unpaid")

    dashboard.mark_invoice_as_paid("INV-1002")

    dashboard.expect_payment_success_message("INV-1002")
    dashboard.expect_invoice_status("INV-1002", "Paid")
    dashboard.expect_mark_as_paid_button_disabled("INV-1002")

    response = invoice_client.get_invoice("INV-1002")

    assert response.status == 200

    invoice = response.json()

    assert invoice["invoice_id"] == "INV-1002"
    assert invoice["status"] == "Paid"