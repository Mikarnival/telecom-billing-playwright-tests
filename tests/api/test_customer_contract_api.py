import pytest

from api_clients.contract_client import ContractClient
from api_clients.customer_client import CustomerClient


@pytest.mark.api
def test_create_customer_returns_active_status(
    customer_client: CustomerClient,
    reset_test_data: None,
) -> None:
    response = customer_client.create_customer(
        customer_id="CUST-100",
        customer_name="Gamma Wireless",
        customer_type="Business",
    )

    assert response.status in (200, 201)

    customer = response.json()

    assert customer["customer_id"] == "CUST-100"
    assert customer["customer_name"] == "Gamma Wireless"
    assert customer["customer_type"] == "Business"
    assert customer["status"] == "Active"


@pytest.mark.api
def test_get_customer_by_id_returns_created_customer(
    customer_client: CustomerClient,
    reset_test_data: None,
) -> None:
    customer_client.create_customer(
        customer_id="CUST-101",
        customer_name="Omega Mobile",
        customer_type="Consumer",
    )

    response = customer_client.get_customer("CUST-101")

    assert response.status == 200

    customer = response.json()

    assert customer["customer_id"] == "CUST-101"
    assert customer["customer_name"] == "Omega Mobile"
    assert customer["customer_type"] == "Consumer"
    assert customer["status"] == "Active"


@pytest.mark.api
def test_get_unknown_customer_returns_404(
    customer_client: CustomerClient,
    reset_test_data: None,
) -> None:
    response = customer_client.get_customer("CUST-999")

    assert response.status == 404

    body = response.json()

    assert "not found" in body["detail"]


@pytest.mark.api
def test_create_contract_for_existing_customer_returns_draft_status(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    response = contract_client.create_contract(
        contract_id="CON-9001",
        customer_id="CUST-001",
        plan="Roaming Business",
    )

    assert response.status in (200, 201)

    contract = response.json()

    assert contract["contract_id"] == "CON-9001"
    assert contract["customer_id"] == "CUST-001"
    assert contract["plan"] == "Roaming Business"
    assert contract["status"] == "Draft"


@pytest.mark.api
def test_get_contract_by_id_returns_created_contract(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    contract_client.create_contract(
        contract_id="CON-9002",
        customer_id="CUST-002",
        plan="Fiber Plus",
    )

    response = contract_client.get_contract("CON-9002")

    assert response.status == 200

    contract = response.json()

    assert contract["contract_id"] == "CON-9002"
    assert contract["customer_id"] == "CUST-002"
    assert contract["plan"] == "Fiber Plus"
    assert contract["status"] == "Draft"


@pytest.mark.api
def test_activate_draft_contract_changes_status_to_active(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    contract_client.create_contract(
        contract_id="CON-9003",
        customer_id="CUST-003",
        plan="Mobile Enterprise",
    )

    response = contract_client.activate_contract("CON-9003")

    assert response.status == 200

    contract = response.json()

    assert contract["contract_id"] == "CON-9003"
    assert contract["status"] == "Active"


@pytest.mark.api
def test_activate_already_active_contract_keeps_status_active(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    contract_client.create_contract(
        contract_id="CON-9004",
        customer_id="CUST-001",
        plan="5G Premium",
    )
    contract_client.activate_contract("CON-9004")

    response = contract_client.activate_contract("CON-9004")

    assert response.status == 200

    contract = response.json()

    assert contract["contract_id"] == "CON-9004"
    assert contract["status"] == "Active"


@pytest.mark.api
def test_create_contract_for_unknown_customer_returns_404(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    response = contract_client.create_contract(
        contract_id="CON-9999",
        customer_id="CUST-999",
        plan="Unknown Plan",
    )

    assert response.status == 404

    body = response.json()

    assert "not found" in body["detail"]


@pytest.mark.api
def test_activate_unknown_contract_returns_404(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    response = contract_client.activate_contract("CON-9999")

    assert response.status == 404

    body = response.json()

    assert "not found" in body["detail"]


@pytest.mark.api
def test_reset_endpoint_resets_customers_and_contracts_to_initial_state(
    customer_client: CustomerClient,
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    customer_client.create_customer(
        customer_id="CUST-200",
        customer_name="Reset Customer",
        customer_type="Business",
    )
    contract_client.create_contract(
        contract_id="CON-9200",
        customer_id="CUST-200",
        plan="Reset Plan",
    )
    contract_client.activate_contract("CON-5002")

    reset_response = customer_client.reset_data()

    assert reset_response.ok

    created_customer_response = customer_client.get_customer("CUST-200")
    created_contract_response = contract_client.get_contract("CON-9200")
    initial_customer_response = customer_client.get_customer("CUST-001")
    initial_contract_response = contract_client.get_contract("CON-5002")

    assert created_customer_response.status == 404
    assert created_contract_response.status == 404
    assert initial_customer_response.status == 200
    assert initial_contract_response.status == 200

    initial_customer = initial_customer_response.json()
    initial_contract = initial_contract_response.json()

    assert initial_customer["customer_id"] == "CUST-001"
    assert initial_customer["status"] == "Active"
    assert initial_contract["contract_id"] == "CON-5002"
    assert initial_contract["status"] == "Active"
