from playwright.sync_api import APIRequestContext, APIResponse


class InvoiceClient:
    def __init__(self, api_context: APIRequestContext) -> None:
        self.api_context = api_context

    def health_check(self) -> APIResponse:
        return self.api_context.get("/health")

    def reset_data(self) -> APIResponse:
        return self.api_context.post("/api/test/reset")

    def list_invoices(self) -> APIResponse:
        return self.api_context.get("/api/invoices")

    def search_invoices(self, query: str) -> APIResponse:
        return self.api_context.get(
            "/api/invoices",
            params={"query": query},
        )

    def filter_invoices_by_status(self, status: str) -> APIResponse:
        return self.api_context.get(
            "/api/invoices",
            params={"status": status},
        )

    def get_invoice(self, invoice_id: str) -> APIResponse:
        return self.api_context.get(f"/api/invoices/{invoice_id}")

    def mark_as_paid(self, invoice_id: str) -> APIResponse:
        return self.api_context.patch(f"/api/invoices/{invoice_id}/pay")