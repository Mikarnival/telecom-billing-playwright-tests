from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.backend.data import (
    get_all_invoices,
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