from playwright.sync_api import APIRequestContext, APIResponse


class BillingRunClient:
    def __init__(self, api_context: APIRequestContext) -> None:
        self.api_context = api_context

    def create_billing_run(self, billing_period: str) -> APIResponse:
        return self.api_context.post(
            "/api/billing-runs",
            data={
                "billing_period": billing_period,
            },
        )

    def get_billing_run(self, billing_run_id: str) -> APIResponse:
        return self.api_context.get(f"/api/billing-runs/{billing_run_id}")
