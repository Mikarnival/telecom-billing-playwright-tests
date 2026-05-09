import pytest
from playwright.sync_api import Page

from pages.billing_dashboard_page import BillingDashboardPage


@pytest.mark.ui
@pytest.mark.smoke
def test_dashboard_loads_invoice_table(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.expect_invoice_visible("INV-1001")
    dashboard.expect_invoice_visible("INV-1002")
    dashboard.expect_invoice_visible("INV-1003")

    dashboard.expect_invoice_contains("INV-1001", "Alice Mobile")
    dashboard.expect_invoice_contains("INV-1001", "$89.00")
    dashboard.expect_invoice_contains("INV-1001", "Paid")

    dashboard.expect_invoice_contains("INV-1002", "Beta Telecom")
    dashboard.expect_invoice_contains("INV-1002", "$249.00")
    dashboard.expect_invoice_contains("INV-1002", "Unpaid")

    dashboard.expect_invoice_contains("INV-1003", "Delta GmbH")
    dashboard.expect_invoice_contains("INV-1003", "$399.00")
    dashboard.expect_invoice_contains("INV-1003", "Overdue")


@pytest.mark.ui
@pytest.mark.smoke
def test_search_customer_shows_matching_invoice_only(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.search_invoice("Beta")

    dashboard.expect_invoice_visible("INV-1002")
    dashboard.expect_invoice_not_present("INV-1001")
    dashboard.expect_invoice_not_present("INV-1003")

    dashboard.expect_invoice_contains("INV-1002", "Beta Telecom")
    dashboard.expect_invoice_contains("INV-1002", "Fiber Business")
    dashboard.expect_invoice_contains("INV-1002", "$249.00")
    dashboard.expect_invoice_contains("INV-1002", "Unpaid")


@pytest.mark.ui
def test_search_invoice_by_invoice_id(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.search_invoice("INV-1003")

    dashboard.expect_invoice_visible("INV-1003")
    dashboard.expect_invoice_not_present("INV-1001")
    dashboard.expect_invoice_not_present("INV-1002")

    dashboard.expect_invoice_contains("INV-1003", "Delta GmbH")
    dashboard.expect_invoice_contains("INV-1003", "Business Mobile")
    dashboard.expect_invoice_contains("INV-1003", "$399.00")
    dashboard.expect_invoice_contains("INV-1003", "Overdue")


@pytest.mark.ui
@pytest.mark.smoke
def test_filter_unpaid_invoices(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.filter_by_status("Unpaid")

    dashboard.expect_invoice_visible("INV-1002")
    dashboard.expect_invoice_not_present("INV-1001")
    dashboard.expect_invoice_not_present("INV-1003")

    dashboard.expect_invoice_contains("INV-1002", "Beta Telecom")
    dashboard.expect_invoice_contains("INV-1002", "Unpaid")


@pytest.mark.ui
def test_filter_paid_invoices(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.filter_by_status("Paid")

    dashboard.expect_invoice_visible("INV-1001")
    dashboard.expect_invoice_not_present("INV-1002")
    dashboard.expect_invoice_not_present("INV-1003")

    dashboard.expect_invoice_contains("INV-1001", "Alice Mobile")
    dashboard.expect_invoice_contains("INV-1001", "Paid")


@pytest.mark.ui
def test_filter_overdue_invoices(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.filter_by_status("Overdue")

    dashboard.expect_invoice_visible("INV-1003")
    dashboard.expect_invoice_not_present("INV-1001")
    dashboard.expect_invoice_not_present("INV-1002")

    dashboard.expect_invoice_contains("INV-1003", "Delta GmbH")
    dashboard.expect_invoice_contains("INV-1003", "Overdue")


@pytest.mark.ui
@pytest.mark.smoke
def test_user_can_mark_unpaid_invoice_as_paid(
    page: Page,
    frontend_base_url: str,
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