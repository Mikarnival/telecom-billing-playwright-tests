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
    dashboard.expect_invoice_contains("INV-1001", "€89.00")
    dashboard.expect_invoice_contains("INV-1001", "Paid")

    dashboard.expect_invoice_contains("INV-1002", "Beta Telecom")
    dashboard.expect_invoice_contains("INV-1002", "€249.00")
    dashboard.expect_invoice_contains("INV-1002", "Unpaid")

    dashboard.expect_invoice_contains("INV-1003", "Delta GmbH")
    dashboard.expect_invoice_contains("INV-1003", "€399.00")
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
    dashboard.expect_invoice_contains("INV-1002", "€249.00")
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
    dashboard.expect_invoice_contains("INV-1003", "€399.00")
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


@pytest.mark.ui
def test_paid_invoice_shows_low_risk(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.expect_invoice_risk("INV-1001", "Low Risk")


@pytest.mark.ui
def test_unpaid_invoice_shows_medium_risk(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.expect_invoice_risk("INV-1002", "Medium Risk")


@pytest.mark.ui
def test_overdue_invoice_shows_high_risk(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.expect_invoice_risk("INV-1003", "High Risk")


@pytest.mark.ui
def test_billing_operations_section_loads(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.expect_billing_operations_visible()


@pytest.mark.ui
def test_user_can_run_monthly_billing_from_ui(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.run_monthly_billing("2026-08")

    dashboard.expect_billing_success_message("BR-2026-08")


@pytest.mark.ui
def test_generated_invoice_appears_with_medium_risk_after_billing_run(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    dashboard = BillingDashboardPage(page, frontend_base_url)

    dashboard.open()
    dashboard.expect_loaded()

    dashboard.run_monthly_billing("2026-08")

    dashboard.expect_billing_success_message("BR-2026-08")
    dashboard.expect_invoice_visible("INV-202608-CON-5001")
    dashboard.expect_invoice_risk("INV-202608-CON-5001", "Medium Risk")
