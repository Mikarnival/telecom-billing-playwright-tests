from playwright.sync_api import APIRequestContext, APIResponse


class CustomerClient:
    def __init__(self, api_context: APIRequestContext) -> None:
        self.api_context = api_context

    def reset_data(self) -> APIResponse:
        return self.api_context.post("/api/test/reset")

    def create_customer(
        self,
        customer_id: str,
        customer_name: str,
        customer_type: str,
    ) -> APIResponse:
        return self.api_context.post(
            "/api/customers",
            data={
                "customer_id": customer_id,
                "customer_name": customer_name,
                "customer_type": customer_type,
            },
        )

    def get_customer(self, customer_id: str) -> APIResponse:
        return self.api_context.get(f"/api/customers/{customer_id}")
