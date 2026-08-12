from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright

from config.settings import settings

from api_clients.billing_run_client import BillingRunClient
from api_clients.contract_client import ContractClient
from api_clients.customer_client import CustomerClient
from api_clients.invoice_client import InvoiceClient


@pytest.fixture(scope="session")
def frontend_base_url() -> str:
    return settings.frontend_base_url


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return settings.api_base_url


@pytest.fixture
def api_context(
    playwright: Playwright,
    api_base_url: str,
) -> Generator[APIRequestContext, None, None]:
    context = playwright.request.new_context(
        base_url=api_base_url,
        timeout=settings.api_timeout_ms,
    )

    yield context

    context.dispose()


@pytest.fixture
def configured_page(page: Page) -> Page:
    page.set_default_timeout(settings.ui_timeout_ms)
    return page


@pytest.fixture
def reset_test_data(api_context: APIRequestContext) -> None:
    response = api_context.post("/api/test/reset")
    assert response.ok


@pytest.fixture
def invoice_client(api_context: APIRequestContext) -> InvoiceClient:
    return InvoiceClient(api_context)


@pytest.fixture
def customer_client(api_context: APIRequestContext) -> CustomerClient:
    return CustomerClient(api_context)


@pytest.fixture
def contract_client(api_context: APIRequestContext) -> ContractClient:
    return ContractClient(api_context)


@pytest.fixture
def billing_run_client(api_context: APIRequestContext) -> BillingRunClient:
    return BillingRunClient(api_context)
