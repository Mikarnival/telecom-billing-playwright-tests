from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.backend.data import (
    activate_contract,
    create_billing_run,
    create_contract,
    create_customer,
    get_all_invoices,
    get_billing_run_by_id,
    get_contract_by_id,
    get_customer_by_id,
    get_invoice_by_id,
    mark_invoice_as_paid,
    reset_data,
    search_invoices,
)


app = FastAPI(
    title="Mini Telecom Billing API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/test/reset")
def reset_test_data() -> dict[str, str]:
    reset_data()
    return {"status": "reset"}


@app.get("/api/invoices")
def list_invoices(
    query: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> list[dict]:
    if query or status:
        return search_invoices(query=query, status=status)

    return get_all_invoices()


@app.get("/api/invoices/{invoice_id}")
def get_invoice(invoice_id: str) -> dict:
    invoice = get_invoice_by_id(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invoice {invoice_id} not found",
        )

    return invoice


@app.patch("/api/invoices/{invoice_id}/pay")
def pay_invoice(invoice_id: str) -> dict:
    invoice = mark_invoice_as_paid(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invoice {invoice_id} not found",
        )

    return invoice


@app.post("/api/customers")
def add_customer(customer_data: dict) -> dict:
    return create_customer(customer_data)


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str) -> dict:
    customer = get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    return customer


@app.post("/api/contracts")
def add_contract(contract_data: dict) -> dict:
    contract = create_contract(contract_data)

    if contract is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {contract_data['customer_id']} not found",
        )

    return contract


@app.get("/api/contracts/{contract_id}")
def get_contract(contract_id: str) -> dict:
    contract = get_contract_by_id(contract_id)

    if contract is None:
        raise HTTPException(
            status_code=404,
            detail=f"Contract {contract_id} not found",
        )

    return contract


@app.patch("/api/contracts/{contract_id}/activate")
def activate_existing_contract(contract_id: str) -> dict:
    contract = activate_contract(contract_id)

    if contract is None:
        raise HTTPException(
            status_code=404,
            detail=f"Contract {contract_id} not found",
        )

    return contract


@app.post("/api/billing-runs")
def add_billing_run(billing_run_data: dict) -> dict:
    return create_billing_run(billing_run_data["billing_period"])


@app.get("/api/billing-runs/{billing_run_id}")
def get_billing_run(billing_run_id: str) -> dict:
    billing_run = get_billing_run_by_id(billing_run_id)

    if billing_run is None:
        raise HTTPException(
            status_code=404,
            detail=f"Billing run {billing_run_id} not found",
        )

    return billing_run
