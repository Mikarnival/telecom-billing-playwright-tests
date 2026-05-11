import pytest
from playwright.sync_api import Page, Route

from pages.customer_contract_page import CustomerContractPage


@pytest.mark.ui
def test_customer_contract_section_loads(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()
    lifecycle.expect_customer_not_found_message()


@pytest.mark.ui
def test_search_existing_customer_by_customer_id(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()

    lifecycle.search_customer("CUST-002")

    lifecycle.expect_customer_visible("CUST-002")
    lifecycle.expect_customer_fields(
        customer_id="CUST-002",
        customer_name="Beta Telecom",
        customer_type="Business",
        status="Active",
    )


@pytest.mark.ui
def test_search_unknown_customer_shows_no_customer_found(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()

    lifecycle.search_customer("CUST-999")

    lifecycle.expect_customer_not_found_message()


@pytest.mark.ui
def test_existing_customer_shows_related_contract(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()

    lifecycle.search_customer("CUST-002")

    lifecycle.expect_contract_fields(
        contract_id="CON-5002",
        plan="Fiber Business",
        status="Active",
    )


@pytest.mark.ui
def test_draft_contract_can_be_activated_from_ui(
    page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    page.request.post(
        "http://localhost:8000/api/contracts",
        data={
            "contract_id": "CON-9005",
            "customer_id": "CUST-002",
            "plan": "Fiber Trial",
        },
    )

    def route_customer_invoice_search(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body=(
                '[{"invoice_id":"INV-9005","customer_id":"CUST-002",'
                '"customer_name":"Beta Telecom","contract_id":"CON-9005",'
                '"plan":"Fiber Trial","amount":0,"status":"Unpaid",'
                '"billing_period":"2026-05"}]'
            ),
        )

    page.route(
        "**/api/invoices?query=CUST-002",
        route_customer_invoice_search,
    )

    lifecycle = CustomerContractPage(page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()

    lifecycle.search_customer("CUST-002")

    lifecycle.expect_contract_fields(
        contract_id="CON-9005",
        plan="Fiber Trial",
        status="Draft",
    )

    lifecycle.activate_contract("CON-9005")

    lifecycle.expect_contract_status("CON-9005", "Active")
