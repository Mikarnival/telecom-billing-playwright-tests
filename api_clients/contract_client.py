from playwright.sync_api import APIRequestContext, APIResponse


class ContractClient:
    def __init__(self, api_context: APIRequestContext) -> None:
        self.api_context = api_context

    def create_contract(
        self,
        contract_id: str,
        customer_id: str,
        plan: str,
    ) -> APIResponse:
        return self.api_context.post(
            "/api/contracts",
            data={
                "contract_id": contract_id,
                "customer_id": customer_id,
                "plan": plan,
            },
        )

    def get_contract(self, contract_id: str) -> APIResponse:
        return self.api_context.get(f"/api/contracts/{contract_id}")

    def activate_contract(self, contract_id: str) -> APIResponse:
        return self.api_context.patch(f"/api/contracts/{contract_id}/activate")
