import json

import pytest
from playwright.sync_api import Page, Route

from api_clients.contract_client import ContractClient
from api_clients.customer_client import CustomerClient
from pages.customer_contract_page import CustomerContractPage


@pytest.mark.e2e
@pytest.mark.smoke
def test_activate_draft_contract_from_ui_and_verify_by_api(
    page: Page,
    frontend_base_url: str,
    customer_client: CustomerClient,
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    customer_response = customer_client.create_customer(
        customer_id="CUST-300",
        customer_name="Epsilon Networks",
        customer_type="Business",
    )
    contract_response = contract_client.create_contract(
        contract_id="CON-9300",
        customer_id="CUST-300",
        plan="Fiber Enterprise Trial",
    )

    assert customer_response.status in (200, 201)
    assert contract_response.status in (200, 201)

    def route_customer_invoice_search(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(
                [
                    {
                        "invoice_id": "INV-9300",
                        "customer_id": "CUST-300",
                        "customer_name": "Epsilon Networks",
                        "contract_id": "CON-9300",
                        "plan": "Fiber Enterprise Trial",
                        "amount": 0,
                        "status": "Unpaid",
                        "billing_period": "2026-05",
                    }
                ]
            ),
        )

    page.route(
        "**/api/invoices?query=CUST-300",
        route_customer_invoice_search,
    )

    lifecycle = CustomerContractPage(page, frontend_base_url)

    lifecycle.open()
    lifecycle.expect_loaded()

    lifecycle.search_customer("CUST-300")

    lifecycle.expect_customer_visible("CUST-300")
    lifecycle.expect_contract_fields(
        contract_id="CON-9300",
        plan="Fiber Enterprise Trial",
        status="Draft",
    )

    lifecycle.activate_contract("CON-9300")

    lifecycle.expect_contract_status("CON-9300", "Active")

    response = contract_client.get_contract("CON-9300")

    assert response.status == 200

    contract = response.json()

    assert contract["contract_id"] == "CON-9300"
    assert contract["status"] == "Active"
