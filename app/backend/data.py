from copy import deepcopy
from typing import Any


INITIAL_INVOICES: list[dict[str, Any]] = [
    {
        "invoice_id": "INV-1001",
        "customer_id": "CUST-001",
        "customer_name": "Alice Mobile",
        "contract_id": "CON-5001",
        "plan": "5G Unlimited",
        "amount": 89.00,
        "status": "Paid",
        "billing_period": "2026-05",
    },
    {
        "invoice_id": "INV-1002",
        "customer_id": "CUST-002",
        "customer_name": "Beta Telecom",
        "contract_id": "CON-5002",
        "plan": "Fiber Business",
        "amount": 249.00,
        "status": "Unpaid",
        "billing_period": "2026-05",
    },
    {
        "invoice_id": "INV-1003",
        "customer_id": "CUST-003",
        "customer_name": "Delta GmbH",
        "contract_id": "CON-5003",
        "plan": "Business Mobile",
        "amount": 399.00,
        "status": "Overdue",
        "billing_period": "2026-05",
    },
]


INITIAL_CUSTOMERS: list[dict[str, Any]] = [
    {
        "customer_id": "CUST-001",
        "customer_name": "Alice Mobile",
        "customer_type": "Private",
        "status": "Active",
    },
    {
        "customer_id": "CUST-002",
        "customer_name": "Beta Telecom",
        "customer_type": "Business",
        "status": "Active",
    },
    {
        "customer_id": "CUST-003",
        "customer_name": "Delta GmbH",
        "customer_type": "Business",
        "status": "Active",
    },
]


INITIAL_CONTRACTS: list[dict[str, Any]] = [
    {
        "contract_id": "CON-5001",
        "customer_id": "CUST-001",
        "plan": "5G Unlimited",
        "status": "Active",
    },
    {
        "contract_id": "CON-5002",
        "customer_id": "CUST-002",
        "plan": "Fiber Business",
        "status": "Active",
    },
    {
        "contract_id": "CON-5003",
        "customer_id": "CUST-003",
        "plan": "Business Mobile",
        "status": "Active",
    },
]


INITIAL_BILLING_RUNS: list[dict[str, Any]] = []

PLAN_AMOUNTS: dict[str, float] = {
    "5G Unlimited": 89.00,
    "Fiber Business": 249.00,
    "Business Mobile": 399.00,
}


invoices: list[dict[str, Any]] = deepcopy(INITIAL_INVOICES)
customers: list[dict[str, Any]] = deepcopy(INITIAL_CUSTOMERS)
contracts: list[dict[str, Any]] = deepcopy(INITIAL_CONTRACTS)
billing_runs: list[dict[str, Any]] = deepcopy(INITIAL_BILLING_RUNS)


def reset_data() -> None:
    """
    Reset mock data to its initial state.
    Useful for tests, so each test starts from the same data.
    """
    global invoices, customers, contracts, billing_runs
    invoices = deepcopy(INITIAL_INVOICES)
    customers = deepcopy(INITIAL_CUSTOMERS)
    contracts = deepcopy(INITIAL_CONTRACTS)
    billing_runs = deepcopy(INITIAL_BILLING_RUNS)


def get_all_invoices() -> list[dict[str, Any]]:
    return invoices


def get_invoice_by_id(invoice_id: str) -> dict[str, Any] | None:
    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return None


def search_invoices(query: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
    result = invoices

    if query:
        normalized_query = query.lower()
        result = [
            invoice
            for invoice in result
            if normalized_query in invoice["invoice_id"].lower()
            or normalized_query in invoice["customer_name"].lower()
            or normalized_query in invoice["customer_id"].lower()
        ]

    if status:
        normalized_status = status.lower()
        result = [
            invoice
            for invoice in result
            if invoice["status"].lower() == normalized_status
        ]

    return result


def mark_invoice_as_paid(invoice_id: str) -> dict[str, Any] | None:
    invoice = get_invoice_by_id(invoice_id)

    if invoice is None:
        return None

    invoice["status"] = "Paid"
    return invoice


def create_customer(customer_data: dict[str, Any]) -> dict[str, Any]:
    customer = {
        "customer_id": customer_data["customer_id"],
        "customer_name": customer_data["customer_name"],
        "customer_type": customer_data["customer_type"],
        "status": "Active",
    }

    customers.append(customer)
    return customer


def get_customer_by_id(customer_id: str) -> dict[str, Any] | None:
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer
    return None


def create_contract(contract_data: dict[str, Any]) -> dict[str, Any] | None:
    customer = get_customer_by_id(contract_data["customer_id"])

    if customer is None:
        return None

    contract = {
        "contract_id": contract_data["contract_id"],
        "customer_id": contract_data["customer_id"],
        "plan": contract_data["plan"],
        "status": "Draft",
    }

    contracts.append(contract)
    return contract


def get_contract_by_id(contract_id: str) -> dict[str, Any] | None:
    for contract in contracts:
        if contract["contract_id"] == contract_id:
            return contract
    return None


def activate_contract(contract_id: str) -> dict[str, Any] | None:
    contract = get_contract_by_id(contract_id)

    if contract is None:
        return None

    contract["status"] = "Active"
    return contract


def get_billing_run_by_id(billing_run_id: str) -> dict[str, Any] | None:
    for billing_run in billing_runs:
        if billing_run["billing_run_id"] == billing_run_id:
            return billing_run
    return None


def get_billing_run_by_period(billing_period: str) -> dict[str, Any] | None:
    billing_run_id = f"BR-{billing_period}"
    return get_billing_run_by_id(billing_run_id)


def create_billing_run(billing_period: str) -> dict[str, Any]:
    existing_billing_run = get_billing_run_by_period(billing_period)

    if existing_billing_run is not None:
        return {
            **existing_billing_run,
            "message": (
                f"Billing run for {billing_period} already exists; "
                "no duplicate invoices created."
            ),
        }

    generated_invoice_ids: list[str] = []

    for contract in contracts:
        if contract["status"] != "Active":
            continue

        amount = PLAN_AMOUNTS.get(contract["plan"])
        if amount is None:
            continue

        invoice_id = f"INV-{billing_period.replace('-', '')}-{contract['contract_id']}"
        duplicate_invoice = any(
            invoice["contract_id"] == contract["contract_id"]
            and invoice["billing_period"] == billing_period
            for invoice in invoices
        )

        if duplicate_invoice:
            continue

        customer = get_customer_by_id(contract["customer_id"])
        if customer is None:
            continue

        invoice = {
            "invoice_id": invoice_id,
            "customer_id": customer["customer_id"],
            "customer_name": customer["customer_name"],
            "contract_id": contract["contract_id"],
            "plan": contract["plan"],
            "amount": amount,
            "status": "Unpaid",
            "billing_period": billing_period,
        }

        invoices.append(invoice)
        generated_invoice_ids.append(invoice_id)

    billing_run = {
        "billing_run_id": f"BR-{billing_period}",
        "billing_period": billing_period,
        "generated_invoice_ids": generated_invoice_ids,
        "status": "Completed",
    }

    billing_runs.append(billing_run)
    return billing_run
