import pytest
from playwright.sync_api import APIRequestContext

@pytest.mark.staging
@pytest.mark.smoke
def test_staging_frontend_is_available(
    api_context: APIRequestContext,
) -> None:
    response = api_context.get("/")

    assert response.status == 200

@pytest.mark.staging
@pytest.mark.smoke
def test_staging_invoices_api_is_available(
    api_context: APIRequestContext,
) -> None:
    response = api_context.get("/api/invoices")

    assert response.status == 200

    invoices = response.json()

    assert isinstance(invoices, list)
    assert len(invoices) > 0