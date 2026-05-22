from typing import Any

import requests
from mcp.server.fastmcp import FastMCP


BACKEND_BASE_URL = "http://localhost:8000"
BACKEND_TIMEOUT_SECONDS = 5

mcp = FastMCP(
    "Telecom Billing Invoice Lookup",
    host="localhost",
    port=8001,
    stateless_http=True,
    json_response=True,
)


def _error_result(
    code: str,
    message: str,
    invoice_id: str,
    status_code: int | None = None,
) -> dict[str, Any]:
    error: dict[str, Any] = {
        "code": code,
        "message": message,
        "invoice_id": invoice_id,
    }

    if status_code is not None:
        error["status_code"] = status_code

    return {"error": error}


@mcp.tool()
def get_invoice(invoice_id: str) -> dict[str, Any]:
    """Return one invoice from the telecom billing backend by invoice ID."""
    try:
        response = requests.get(
            f"{BACKEND_BASE_URL}/api/invoices/{invoice_id}",
            timeout=BACKEND_TIMEOUT_SECONDS,
        )
    except requests.exceptions.ConnectionError:
        return _error_result(
            code="backend_unavailable",
            message=(
                "Backend connection failed. Start the FastAPI backend before "
                "using this MCP tool: uvicorn app.backend.main:app --reload --port 8000"
            ),
            invoice_id=invoice_id,
        )
    except requests.exceptions.RequestException as exc:
        return _error_result(
            code="backend_request_failed",
            message=f"Backend request failed: {exc}",
            invoice_id=invoice_id,
        )

    if response.status_code == 404:
        detail = _response_detail(response)
        return _error_result(
            code="invoice_not_found",
            message=detail or f"Invoice {invoice_id} not found",
            invoice_id=invoice_id,
            status_code=response.status_code,
        )

    if not response.ok:
        return _error_result(
            code="backend_error",
            message=f"Backend returned HTTP {response.status_code}",
            invoice_id=invoice_id,
            status_code=response.status_code,
        )

    return response.json()


def _response_detail(response: requests.Response) -> str | None:
    try:
        body = response.json()
    except ValueError:
        return None

    detail = body.get("detail")
    if isinstance(detail, str):
        return detail

    return None


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
