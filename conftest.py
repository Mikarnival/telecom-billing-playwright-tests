from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from api_clients.contract_client import ContractClient
from api_clients.customer_client import CustomerClient
from api_clients.invoice_client import InvoiceClient


@pytest.fixture(scope="session")
def frontend_base_url() -> str:
    return "http://localhost:3000"


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return "http://localhost:8000"


@pytest.fixture
def api_context(
    playwright: Playwright,
    api_base_url: str,
) -> Generator[APIRequestContext, None, None]:
    context = playwright.request.new_context(
        base_url=api_base_url
    )

    yield context

    context.dispose()


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
