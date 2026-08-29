import re

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BillingDashboardPage:
    INVOICE_TABLE = (
        By.CSS_SELECTOR,
        'table[aria-label="Invoices"]',
    )

    CUSTOMER_SEARCH = (
        By.ID,
        "customer-search",
    )

    STATUS_FILTER = (
        By.ID,
        "status-filter",
    )

    def __init__(
        self,
        driver: WebDriver,
        base_url: str,
    ) -> None:
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        self.driver.get(self.base_url)

    def expect_loaded(self) -> None:
        self.wait.until(
            EC.title_is("Telecom Billing Dashboard")
        )

        heading = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h1[normalize-space()='Telecom Billing Dashboard']",
                )
            )
        )

        assert heading.is_displayed()

    def search_invoice(self, search_text: str) -> None:
        search_input = self.wait.until(
            EC.visibility_of_element_located(
                self.CUSTOMER_SEARCH
            )
        )

        search_input.clear()
        search_input.send_keys(search_text)

    def filter_by_status(self, status: str) -> None:
        status_filter = self.wait.until(
            EC.element_to_be_clickable(
                self.STATUS_FILTER
            )
        )

        Select(status_filter).select_by_visible_text(status)

    def invoice_table(self) -> WebElement:
        return self.wait.until(
            EC.visibility_of_element_located(
                self.INVOICE_TABLE
            )
        )

    def invoice_row(
        self,
        invoice_id: str,
    ) -> WebElement:
        return self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    f'[data-testid="invoice-row-{invoice_id}"]',
                )
            )
        )

    def expect_invoice_visible(
        self,
        invoice_id: str,
    ) -> None:
        row = self.invoice_row(invoice_id)

        assert row.is_displayed()

    def expect_invoice_not_present(
        self,
        invoice_id: str,
    ) -> None:
        locator = (
            By.CSS_SELECTOR,
            f'[data-testid="invoice-row-{invoice_id}"]',
        )

        self.wait.until(
            lambda driver: len(driver.find_elements(*locator)) == 0
        )

    def expect_invoice_contains(
        self,
        invoice_id: str,
        text: str,
    ) -> None:
        row = self.invoice_row(invoice_id)

        self.wait.until(
            lambda driver: text in row.text
        )

        assert text in row.text

    def expect_invoice_status(
        self,
        invoice_id: str,
        status: str,
    ) -> None:
        self.expect_invoice_contains(
            invoice_id,
            status,
        )

    def expect_invoice_risk(
        self,
        invoice_id: str,
        risk: str,
    ) -> None:
        self.expect_invoice_contains(
            invoice_id,
            risk,
        )

    def mark_invoice_as_paid(
        self,
        invoice_id: str,
    ) -> None:
        row = self.invoice_row(invoice_id)

        button = row.find_element(
            By.XPATH,
            ".//button[normalize-space()='Mark as Paid']",
        )

        self.wait.until(
            lambda driver: button.is_displayed()
            and button.is_enabled()
        )

        button.click()

    def expect_payment_success_message(
        self,
        invoice_id: str,
    ) -> None:
        message = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    (
                        "//*[contains("
                        "normalize-space(), "
                        f"'{invoice_id} was marked as paid'"
                        ")]"
                    ),
                )
            )
        )

        assert message.is_displayed()

    def expect_mark_as_paid_button_disabled(
        self,
        invoice_id: str,
    ) -> None:
        row = self.invoice_row(invoice_id)

        button = row.find_element(
            By.XPATH,
            ".//button[normalize-space()='Mark as Paid']",
        )

        self.wait.until(
            lambda driver: not button.is_enabled()
        )

        assert not button.is_enabled()

    def expect_billing_operations_visible(self) -> None:
        heading = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h2[normalize-space()='Billing Operations']",
                )
            )
        )

        billing_period = self._element_by_label(
            "Billing period"
        )

        run_button = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[normalize-space()='Run Monthly Billing']",
                )
            )
        )

        assert heading.is_displayed()
        assert billing_period.is_displayed()
        assert run_button.is_displayed()

    def run_monthly_billing(
        self,
        billing_period: str,
    ) -> None:
        billing_period_input = self._element_by_label(
            "Billing period"
        )

        billing_period_input.clear()
        billing_period_input.send_keys(
            billing_period
        )

        run_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Run Monthly Billing']",
                )
            )
        )

        run_button.click()

    def expect_billing_success_message(
        self,
        billing_run_id: str,
    ) -> None:
        message = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    (
                        "//*[contains("
                        "normalize-space(), "
                        f"'Billing run {billing_run_id} completed'"
                        ")]"
                    ),
                )
            )
        )

        assert message.is_displayed()

    def _element_by_label(
        self,
        label_text: str,
    ) -> WebElement:
        label = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//label[normalize-space()='{label_text}']",
                )
            )
        )

        element_id = label.get_attribute("for")

        if not element_id:
            raise AssertionError(
                f"Label '{label_text}' has no 'for' attribute"
            )

        return self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    element_id,
                )
            )
        )