import pytest
from playwright.sync_api import Page, Route

from pages.customer_contract_page import CustomerContractPage
from api_clients.contract_client import ContractClient

@pytest.mark.ui
def test_customer_contract_section_loads(
    configured_page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(configured_page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()
    lifecycle.expect_customer_not_found_message()


@pytest.mark.ui
def test_search_existing_customer_by_customer_id(
    configured_page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(configured_page, frontend_base_url)

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
    configured_page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(configured_page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()

    lifecycle.search_customer("CUST-999")

    lifecycle.expect_customer_not_found_message()


@pytest.mark.ui
def test_existing_customer_shows_related_contract(
    configured_page: Page,
    frontend_base_url: str,
    reset_test_data: None,
) -> None:
    lifecycle = CustomerContractPage(configured_page, frontend_base_url)

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
    configured_page: Page,
    frontend_base_url: str,
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    response = contract_client.create_contract(
        contract_id="CON-9005",
        customer_id="CUST-002",
        plan="Fiber Trial",
    )

    assert response.status in (200, 201)

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

    configured_page.route(
        "**/api/invoices?query=CUST-002",
        route_customer_invoice_search,
    )

    lifecycle = CustomerContractPage(configured_page, frontend_base_url)

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
