from typing import Any

import requests

from mcp_server.server import get_invoice


class FakeResponse:
    def __init__(self, status_code: int, body: dict[str, Any]) -> None:
        self.status_code = status_code
        self._body = body
        self.ok = 200 <= status_code < 400

    def json(self) -> dict[str, Any]:
        return self._body


def test_get_invoice_returns_backend_invoice(monkeypatch) -> None:
    invoice = {
        "invoice_id": "INV-1002",
        "customer_id": "CUST-002",
        "customer_name": "Beta Telecom",
        "contract_id": "CON-5002",
        "plan": "Fiber Business",
        "amount": 249.00,
        "status": "Unpaid",
        "billing_period": "2026-05",
    }

    def fake_get(url: str, timeout: int) -> FakeResponse:
        assert url == "http://localhost:8000/api/invoices/INV-1002"
        assert timeout == 5
        return FakeResponse(200, invoice)

    monkeypatch.setattr(requests, "get", fake_get)

    assert get_invoice("INV-1002") == invoice


def test_get_invoice_returns_structured_error_for_unknown_invoice(monkeypatch) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        return FakeResponse(404, {"detail": "Invoice INV-9999 not found"})

    monkeypatch.setattr(requests, "get", fake_get)

    result = get_invoice("INV-9999")

    assert result == {
        "error": {
            "code": "invoice_not_found",
            "message": "Invoice INV-9999 not found",
            "invoice_id": "INV-9999",
            "status_code": 404,
        }
    }


def test_get_invoice_returns_structured_error_when_backend_unavailable(monkeypatch) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        raise requests.exceptions.ConnectionError("connection refused")

    monkeypatch.setattr(requests, "get", fake_get)

    result = get_invoice("INV-1002")

    assert result["error"]["code"] == "backend_unavailable"
    assert result["error"]["invoice_id"] == "INV-1002"
    assert "Backend connection failed" in result["error"]["message"]
    assert "uvicorn app.backend.main:app --reload --port 8000" in result["error"]["message"]
