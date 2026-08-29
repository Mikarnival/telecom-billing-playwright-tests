import pytest

from pages.selenium.billing_dashboard_page import BillingDashboardPage


@pytest.mark.selenium
def test_dashboard_loads_in_chrome(
    selenium_billing_dashboard_page: BillingDashboardPage,
) -> None:
    selenium_billing_dashboard_page.open()

    selenium_billing_dashboard_page.expect_loaded()


@pytest.mark.selenium
def test_invoice_search_works_in_chrome(
    selenium_billing_dashboard_page: BillingDashboardPage,
) -> None:
    selenium_billing_dashboard_page.open()

    selenium_billing_dashboard_page.search_invoice("CUST-001")

    selenium_billing_dashboard_page.expect_invoice_visible("INV-1001")