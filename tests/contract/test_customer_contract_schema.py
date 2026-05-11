import pytest

from api_clients.contract_client import ContractClient
from api_clients.customer_client import CustomerClient


@pytest.mark.contract
def test_customer_response_contains_required_fields(
    customer_client: CustomerClient,
    reset_test_data: None,
) -> None:
    response = customer_client.get_customer("CUST-002")

    assert response.status == 200

    customer = response.json()

    required_fields = {
        "customer_id",
        "customer_name",
        "customer_type",
        "status",
    }

    assert required_fields.issubset(customer.keys())


@pytest.mark.contract
def test_customer_response_field_types(
    customer_client: CustomerClient,
    reset_test_data: None,
) -> None:
    response = customer_client.get_customer("CUST-002")

    assert response.status == 200

    customer = response.json()

    assert isinstance(customer["customer_id"], str)
    assert isinstance(customer["customer_name"], str)
    assert isinstance(customer["customer_type"], str)
    assert isinstance(customer["status"], str)


@pytest.mark.contract
def test_customer_status_has_valid_value(
    customer_client: CustomerClient,
    reset_test_data: None,
) -> None:
    response = customer_client.get_customer("CUST-002")

    assert response.status == 200

    customer = response.json()

    allowed_statuses = {"Active", "Inactive"}

    assert customer["status"] in allowed_statuses


@pytest.mark.contract
def test_contract_response_contains_required_fields(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    response = contract_client.get_contract("CON-5002")

    assert response.status == 200

    contract = response.json()

    required_fields = {
        "contract_id",
        "customer_id",
        "plan",
        "status",
    }

    assert required_fields.issubset(contract.keys())


@pytest.mark.contract
def test_contract_response_field_types(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    response = contract_client.get_contract("CON-5002")

    assert response.status == 200

    contract = response.json()

    assert isinstance(contract["contract_id"], str)
    assert isinstance(contract["customer_id"], str)
    assert isinstance(contract["plan"], str)
    assert isinstance(contract["status"], str)


@pytest.mark.contract
def test_contract_status_has_valid_value(
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    response = contract_client.get_contract("CON-5002")

    assert response.status == 200

    contract = response.json()

    allowed_statuses = {"Draft", "Active", "Terminated"}

    assert contract["status"] in allowed_statuses


@pytest.mark.contract
def test_created_contract_references_existing_customer_id(
    customer_client: CustomerClient,
    contract_client: ContractClient,
    reset_test_data: None,
) -> None:
    contract_response = contract_client.create_contract(
        contract_id="CON-9400",
        customer_id="CUST-002",
        plan="Fiber Schema Plan",
    )

    assert contract_response.status in (200, 201)

    contract = contract_response.json()

    customer_response = customer_client.get_customer(contract["customer_id"])

    assert customer_response.status == 200

    customer = customer_response.json()

    assert contract["customer_id"] == customer["customer_id"]
