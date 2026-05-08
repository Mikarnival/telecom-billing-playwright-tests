import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.smoke
def test_dashboard_loads_invoice_table(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    page.goto(frontend_base_url)

    expect(page).to_have_title("Telecom Billing Dashboard")
    expect(page.get_by_role("heading", name="Telecom Billing Dashboard")).to_be_visible()

    invoice_table = page.get_by_role("table", name="Invoices")

    expect(invoice_table.get_by_role("row", name=re.compile("INV-1001"))).to_be_visible()
    expect(invoice_table.get_by_role("row", name=re.compile("INV-1002"))).to_be_visible()
    expect(invoice_table.get_by_role("row", name=re.compile("INV-1003"))).to_be_visible()


@pytest.mark.ui
@pytest.mark.smoke
def test_search_customer_shows_matching_invoice_only(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    page.goto(frontend_base_url)

    page.get_by_label("Search customer or invoice").fill("Beta")

    invoice_table = page.get_by_role("table", name="Invoices")

    expect(invoice_table.get_by_role("row", name=re.compile("INV-1002"))).to_be_visible()
    expect(invoice_table.get_by_role("row", name=re.compile("INV-1001"))).to_have_count(0)
    expect(invoice_table.get_by_role("row", name=re.compile("INV-1003"))).to_have_count(0)

    beta_invoice = page.get_by_test_id("invoice-row-INV-1002")

    expect(beta_invoice).to_contain_text("Beta Telecom")
    expect(beta_invoice).to_contain_text("Fiber Business")
    expect(beta_invoice).to_contain_text("$249.00")
    expect(beta_invoice).to_contain_text("Unpaid")


@pytest.mark.ui
@pytest.mark.smoke
def test_filter_unpaid_invoices(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    page.goto(frontend_base_url)

    page.get_by_label("Invoice status").select_option("Unpaid")

    invoice_table = page.get_by_role("table", name="Invoices")

    expect(invoice_table.get_by_role("row", name=re.compile("INV-1002"))).to_be_visible()
    expect(invoice_table.get_by_role("row", name=re.compile("INV-1001"))).to_have_count(0)
    expect(invoice_table.get_by_role("row", name=re.compile("INV-1003"))).to_have_count(0)

    unpaid_invoice = page.get_by_test_id("invoice-row-INV-1002")

    expect(unpaid_invoice).to_contain_text("Beta Telecom")
    expect(unpaid_invoice).to_contain_text("Unpaid")


@pytest.mark.ui
@pytest.mark.smoke
def test_user_can_mark_unpaid_invoice_as_paid(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    page.goto(frontend_base_url)

    invoice_row = page.get_by_test_id("invoice-row-INV-1002")

    expect(invoice_row).to_contain_text("Unpaid")

    invoice_row.get_by_role("button", name="Mark as Paid").click()

    expect(page.get_by_text("INV-1002 was marked as paid")).to_be_visible()

    updated_invoice_row = page.get_by_test_id("invoice-row-INV-1002")

    expect(updated_invoice_row).to_contain_text("Paid")
    expect(updated_invoice_row.get_by_role("button", name="Mark as Paid")).to_be_disabled()