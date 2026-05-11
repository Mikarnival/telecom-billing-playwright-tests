from playwright.sync_api import Locator, Page, expect


class CustomerContractPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url)

    def expect_loaded(self) -> None:
        expect(self.page).to_have_title("Telecom Billing Dashboard")
        expect(
            self.page.get_by_role(
                "heading",
                name="Customer & Contract Lifecycle",
            )
        ).to_be_visible()

    def search_customer(self, customer_id: str) -> None:
        self.page.get_by_label("Search customer", exact=True).fill(customer_id)

    def customer_row(self, customer_id: str) -> Locator:
        return self.page.get_by_test_id(f"customer-row-{customer_id}")

    def contract_row(self, contract_id: str) -> Locator:
        return self.page.get_by_test_id(f"contract-row-{contract_id}")

    def expect_customer_visible(self, customer_id: str) -> None:
        expect(self.customer_row(customer_id)).to_be_visible()

    def expect_customer_not_found_message(self) -> None:
        expect(self.page.get_by_text("No customer found")).to_be_visible()

    def expect_customer_fields(
        self,
        customer_id: str,
        customer_name: str,
        customer_type: str,
        status: str,
    ) -> None:
        customer_row = self.customer_row(customer_id)

        expect(customer_row).to_contain_text(customer_id)
        expect(customer_row).to_contain_text(customer_name)
        expect(customer_row).to_contain_text(customer_type)
        expect(customer_row).to_contain_text(status)

    def expect_contract_fields(
        self,
        contract_id: str,
        plan: str,
        status: str,
    ) -> None:
        contract_row = self.contract_row(contract_id)

        expect(contract_row).to_contain_text(contract_id)
        expect(contract_row).to_contain_text(plan)
        expect(contract_row).to_contain_text(status)

    def activate_contract(self, contract_id: str) -> None:
        self.contract_row(contract_id).get_by_role(
            "button",
            name="Activate Contract",
        ).click()

    def expect_contract_status(self, contract_id: str, status: str) -> None:
        expect(self.contract_row(contract_id)).to_contain_text(status)
