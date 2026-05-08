import pytest
from playwright.sync_api import APIRequestContext, Page, expect


@pytest.mark.e2e
@pytest.mark.smoke
def test_mark_invoice_as_paid_from_ui_and_verify_by_api(
    page: Page,
    frontend_base_url: str,
    api_context: APIRequestContext,
    reset_test_data: None,
) -> None:
    page.goto(frontend_base_url)

    invoice_row = page.get_by_test_id("invoice-row-INV-1002")

    expect(invoice_row).to_contain_text("Unpaid")

    invoice_row.get_by_role("button", name="Mark as Paid").click()

    expect(page.get_by_text("INV-1002 was marked as paid")).to_be_visible()

    response = api_context.get("/api/invoices/INV-1002")

    assert response.status == 200

    invoice = response.json()

    assert invoice["invoice_id"] == "INV-1002"
    assert invoice["status"] == "Paid"