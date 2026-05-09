import re

from playwright.sync_api import Locator, Page, expect


class BillingDashboardPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url)

    def expect_loaded(self) -> None:
        expect(self.page).to_have_title("Telecom Billing Dashboard")
        expect(
            self.page.get_by_role("heading", name="Telecom Billing Dashboard")
        ).to_be_visible()

    def search_invoice(self, search_text: str) -> None:
        self.page.get_by_label("Search customer or invoice").fill(search_text)

    def filter_by_status(self, status: str) -> None:
        self.page.get_by_label("Invoice status").select_option(status)

    def invoice_table(self) -> Locator:
        return self.page.get_by_role("table", name="Invoices")

    def invoice_row(self, invoice_id: str) -> Locator:
        return self.page.get_by_test_id(f"invoice-row-{invoice_id}")

    def expect_invoice_visible(self, invoice_id: str) -> None:
        expect(
            self.invoice_table().get_by_role("row", name=re.compile(invoice_id))
        ).to_be_visible()

    def expect_invoice_not_present(self, invoice_id: str) -> None:
        expect(
            self.invoice_table().get_by_role("row", name=re.compile(invoice_id))
        ).to_have_count(0)

    def expect_invoice_contains(self, invoice_id: str, text: str) -> None:
        expect(self.invoice_row(invoice_id)).to_contain_text(text)

    def expect_invoice_status(self, invoice_id: str, status: str) -> None:
        expect(self.invoice_row(invoice_id)).to_contain_text(status)

    def mark_invoice_as_paid(self, invoice_id: str) -> None:
        self.invoice_row(invoice_id).get_by_role(
            "button",
            name="Mark as Paid",
        ).click()

    def expect_payment_success_message(self, invoice_id: str) -> None:
        expect(
            self.page.get_by_text(f"{invoice_id} was marked as paid")
        ).to_be_visible()

    def expect_mark_as_paid_button_disabled(self, invoice_id: str) -> None:
        expect(
            self.invoice_row(invoice_id).get_by_role(
                "button",
                name="Mark as Paid",
            )
        ).to_be_disabled()