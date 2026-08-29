import pytest

from pytest_bdd import given, parsers, scenarios, then, when

from pages.selenium.billing_dashboard_page import BillingDashboardPage


scenarios("../../features/invoice_search.feature")

@given("the billing dashboard is open")
def user_on_billing_dashboard_page(
    selenium_billing_dashboard_page: BillingDashboardPage,
) -> None:
    selenium_billing_dashboard_page.open()


@when(
    parsers.parse(
        'I search for customer "{customer_id}"'
    )
)
def search_for_customer(
    selenium_billing_dashboard_page: BillingDashboardPage,
    customer_id: str,
) -> None:
    selenium_billing_dashboard_page.search_invoice(customer_id)


@then(
    parsers.parse(
        'invoice "{invoice_id}" should be visible'
    )
)
def invoice_should_be_visible(
    selenium_billing_dashboard_page: BillingDashboardPage,
    invoice_id: str,
) -> None:
    selenium_billing_dashboard_page.expect_invoice_visible(invoice_id)